-- Shattering Chains paid app. Run AFTER schema.sql (Supabase SQL Editor > New query > Run).
-- Auth: Supabase Auth (email magic link). Billing: Stripe, synced by /api/stripe-webhook.

create extension if not exists "pgcrypto";

-- ---------- Subscriptions (written ONLY by the server with the service_role key) ----------
create table if not exists public.subscriptions (
  user_id                uuid primary key references auth.users(id) on delete cascade,
  stripe_customer_id     text not null,
  stripe_subscription_id text unique,
  tier                   text not null check (tier in ('starter','vault','full')),
  status                 text not null,
  current_period_end     timestamptz,
  cancel_at_period_end   boolean not null default false,
  updated_at             timestamptz not null default now()
);
create index if not exists subscriptions_customer_idx on public.subscriptions (stripe_customer_id);

-- Tier rank: starter=1 (map + tracker), vault=2 (+ prayer vault), full=3 (+ audio devotionals).
-- Returns 0 when the caller has no active/trialing subscription.
create or replace function public.current_tier_rank()
returns int
language sql
stable
security definer
set search_path = public
as $$
  select coalesce((
    select case s.tier when 'starter' then 1 when 'vault' then 2 when 'full' then 3 else 0 end
    from public.subscriptions s
    where s.user_id = auth.uid()
      and s.status in ('active', 'trialing')
      and (s.current_period_end is null or s.current_period_end > now() - interval '3 days')
  ), 0);
$$;
revoke all on function public.current_tier_rank() from public;
grant execute on function public.current_tier_rank() to authenticated;

-- ---------- Daily progress (tracker + map) ----------
create table if not exists public.progress (
  user_id       uuid not null references auth.users(id) on delete cascade,
  day           int  not null check (day between 1 and 30),
  habits        jsonb not null default '[]'::jsonb,   -- array of booleans, one per habit
  prayer_minutes int  not null default 0 check (prayer_minutes between 0 and 600),
  chain_before  int check (chain_before between 1 and 10),
  chain_after   int check (chain_after between 1 and 10),
  completed     boolean not null default false,
  completed_at  timestamptz,
  updated_at    timestamptz not null default now(),
  primary key (user_id, day)
);

-- ---------- Private Prayer Vault ----------
create table if not exists public.vault_entries (
  id         uuid primary key default gen_random_uuid(),
  user_id    uuid not null references auth.users(id) on delete cascade,
  day        int check (day between 1 and 30),
  kind       text not null check (kind in ('journal', 'prayer')),
  body       text not null check (char_length(body) between 1 and 8000),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists vault_entries_user_idx on public.vault_entries (user_id, created_at desc);

-- ---------- Row Level Security ----------
alter table public.subscriptions enable row level security;
alter table public.progress      enable row level security;
alter table public.vault_entries enable row level security;

-- Users can read (never write) their own subscription row.
drop policy if exists "read own subscription" on public.subscriptions;
create policy "read own subscription" on public.subscriptions
  for select to authenticated using (user_id = auth.uid());

-- Progress needs any paid tier.
drop policy if exists "own progress" on public.progress;
create policy "own progress" on public.progress
  for all to authenticated
  using (user_id = auth.uid() and public.current_tier_rank() >= 1)
  with check (user_id = auth.uid() and public.current_tier_rank() >= 1);

-- Vault needs Vault tier or higher.
drop policy if exists "own vault" on public.vault_entries;
create policy "own vault" on public.vault_entries
  for all to authenticated
  using (user_id = auth.uid() and public.current_tier_rank() >= 2)
  with check (user_id = auth.uid() and public.current_tier_rank() >= 2);

revoke all on public.subscriptions from anon, authenticated;
grant select on public.subscriptions to authenticated;
revoke all on public.progress, public.vault_entries from anon;
grant select, insert, update, delete on public.progress, public.vault_entries to authenticated;

-- Keep updated_at fresh.
create or replace function public.touch_updated_at() returns trigger language plpgsql as $$
begin new.updated_at = now(); return new; end $$;
drop trigger if exists progress_touch on public.progress;
create trigger progress_touch before update on public.progress for each row execute function public.touch_updated_at();
drop trigger if exists vault_touch on public.vault_entries;
create trigger vault_touch before update on public.vault_entries for each row execute function public.touch_updated_at();

-- Business view: active subscribers and estimated MRR (prices in USD; edit to match your Stripe prices).
create or replace view public.subscription_metrics as
select
  tier,
  count(*) filter (where status in ('active','trialing')) as active_subscribers,
  count(*) filter (where status in ('active','trialing')) *
    case tier when 'starter' then 5 when 'vault' then 8 else 12 end as est_mrr_usd,
  count(*) filter (where cancel_at_period_end) as set_to_cancel
from public.subscriptions
group by tier;
revoke all on public.subscription_metrics from anon, authenticated;
