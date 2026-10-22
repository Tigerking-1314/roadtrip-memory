---
name: my-ways
description: How to use my roadtrip-memory server (save_favorite, list_favorites). Use when I talk about a road trip or travel and say I liked, loved, or want to revisit a place, or tell you to save or remember one; when I ask what my favorites are; or when I ask where to stop or what I liked somewhere. Not for places that come up in work, school, news, where I grew up, or a class assignment.
---

# My ways: roadtrip-memory

**Purpose:** keep the places I loved on the road, and nothing else.

## When to save, and when not to

Save only when **both** are true:
1. We're talking about travel or a road trip (one I'm on, one I took,
   or one I'm planning).
2. I clearly say I like a place or want to go back. "Save it" or
   "remember it" counts.

If a place comes up in any other context, save nothing: work, school,
the news, where I grew up, a restaurant review for a class. Don't
offer to save it, either.

**When unsure, ask me before saving.**

## How to save

1. Call `list_favorites` first. If the place is already there, show me
   the existing entry and ask whether to add another.
2. Show me the `place` and `reason` you're about to save, and wait for
   my OK. Never save without it.
3. `reason` is my own words, trimmed to one line. Don't make up reasons
   I didn't give.
4. After saving, a one-line confirmation is enough.

## Reading my favorites

- When I ask where to stop, or what I liked near somewhere, check
  `list_favorites` before suggesting anything new.
- Otherwise, don't list my favorites unless I ask.

## Examples

- "I love the Grand Canyon, save it." → propose: Grand Canyon, "I love it." Wait for OK.
- "We just left Big Sur. Beautiful coast. Remember it." → propose: Big Sur, "Beautiful coast." Wait for OK.
- "Planning a trip to Utah. Add Zion, I liked the hiking." → propose: Zion, "Liked the hiking." Wait for OK.
- "My professor grew up near Big Sur." → do nothing.
