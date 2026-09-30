-- Shattering Chains lead funnel. Run in Supabase: SQL Editor > New query > Run.

create extension if not exists "pgcrypto";

create table if not exists public.leads_funnel (
  id              uuid primary key default gen_random_uuid(),
  email           text not null,
  name            text not null,
  social_handle   text,
  source_platform text not null default 'direct',
  pdf_downloaded  boolean not null default false,
  app_clicked     boolean not null default false,
  "timestamp"     timestamptz not null default now(),
  constraint leads_funnel_email_key unique (email),
  constraint leads_funnel_email_format check (email = lower(email) and email ~ '^[^@\s]+@[^@\s]+\.[^@\s]+$'),
  constraint leads_funnel_source_check check (source_platform in ('instagram','tiktok','facebook','youtube','direct','other'))
);

create index if not exists leads_funnel_timestamp_idx on public.leads_funnel ("timestamp" desc);
create index if not exists leads_funnel_source_idx on public.leads_funnel (source_platform);

-- Lock the table down: only the server (service_role key, which bypasses RLS) may touch it.
alter table public.leads_funnel enable row level security;
revoke all on public.leads_funnel from anon, authenticated;

-- Live-audit view for the Supabase dashboard / SQL editor.
create or replace view public.leads_funnel_metrics as
select
  source_platform,
  count(*)                                             as leads,
  count(*) filter (where pdf_downloaded)               as pdf_downloads,
  count(*) filter (where app_clicked)                  as app_clicks,
  round(100.0 * count(*) filter (where app_clicked) / nullif(count(*), 0), 1) as app_click_rate_pct,
  min("timestamp")                                     as first_lead,
  max("timestamp")                                     as latest_lead
from public.leads_funnel
group by source_platform
order by leads desc;

revoke all on public.leads_funnel_metrics from anon, authenticated;
