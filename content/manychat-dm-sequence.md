# ManyChat Automation: Comment "SHATTER" -> DM -> Landing Page

Works with Instagram (comment-to-DM) via ManyChat's Meta integration. Facebook Page comments work the same way. TikTok has no comment-to-DM automation in ManyChat: on TikTok, put the landing link in your bio and pin a comment saying "Link in bio -> tap SHATTER".

## Flow layout

```
[TRIGGER]  Instagram: User comments on a Post/Reel
           Keyword: SHATTER   (match: "contains", case-insensitive)
           Scope: this Reel (or "Any post or reel" so every video works)
      |
      v
[ACTION 1] Public reply to comment (rotate randomly, avoids spam flags)
           - "Check your DMs! 🔥"
           - "Sent! Look in your inbox 🙏"
           - "It's on the way, check your DMs ⚓"
      |
      v
[MESSAGE 1 - INSTANT]  Private reply DM (see below)
      |
      v
[ACTION 2] Set Custom User Field  source_platform = instagram
[ACTION 3] Add Tag  shatter_kit_requested
```

## Message 1 (Instant)

**Text:**
> Check your DMs! Your raw 7-Day Shattering Chains A5 Insert Kit is ready. Hit the link below to drop your email, download the PDF instantly, and grab your printables.

**Button** (high-contrast; name it in caps, the DM button label max is 20 chars):
- **Label:** `GET MY KIT NOW`
- **Type:** Open Website
- **URL:**

```
https://YOUR-DOMAIN.vercel.app/?src=instagram&h={{ig_username}}&n={{first_name}}&utm_campaign=shatter_reel
```

The landing page reads these params:

| Param | Stored in | Meaning |
|---|---|---|
| `src` (or `utm_source`) | `source_platform` | `instagram`, `facebook`, `tiktok`, `youtube`, `direct` |
| `h` | `social_handle` | Their IG username (ManyChat merge field) |
| `n` | prefills the name box | Their first name |

> In the ManyChat message editor, insert the merge fields with the **{ } "User Field"** picker rather than typing them (Instagram Username and First Name are System Fields). If a field is empty, the landing page ignores it, so nothing breaks.

For a Facebook flow, duplicate the automation and change `src=instagram` to `src=facebook`.

## Meta rules to keep the account safe

- The comment-triggered DM (a *private reply*) must be sent within 7 days of the comment and Meta allows one private reply per comment. That is why the button lives in Message 1.
- The person did opt in by commenting; still add "Unsubscribe anytime" on the page (already included).
- Don't add more than one follow-up message unless the person replies (24-hour messaging window).

## Optional follow-up (only if they reply or click)

Add a ManyChat "Wait 24 hours -> if Tag `shatter_kit_requested` and not `kit_downloaded`" branch. Because ManyChat can't see the landing-page outcome, use the Google Sheet for auditing instead of a second automated nudge. Manual follow-up copy:

> Did the kit come through okay? Reply YES and I'll re-send it. Day 1 takes 5 minutes. 🔥
