"""7HE H0LY REUP - 5-day devotional blueprint builder.

Builds devotional_blueprint.json: one entry per day with a hook, a "me too"
line, a verified ESV passage, a plain-language teaching note, one soft action,
and an image prompt for a printable coloring page.

Every entry labels what kind of statement it is, so nothing gets passed off as
more than it is:
  scripture    = the quoted text (ESV)
  teaching     = what the passage says in its own context
  application  = interpretation / how it can be used today
  symbolism    = creative imagery, not a claim about the spiritual realm
"""

import json
import os

BRAND = "7HE H0LY REUP"
TRANSLATION = "ESV"

DISCLAIMER = (
    f"{BRAND} is a faith-based encouragement and practice tool. It is not "
    "medical care, addiction treatment, counseling, or crisis support, and "
    "prayer is not a replacement for any of them. If you are in danger, call "
    "911. For crisis support in the U.S., call or text 988. For substance "
    "use support, call SAMHSA at 1-800-662-4357. For abuse or domestic "
    "violence, call the National Domestic Violence Hotline at 1-800-799-7233 "
    "(or text START to 88788)."
)

DEVOTIONAL_MATRIX = {
    1: {
        "title": "The Bathroom Floor",
        "hook": "That floor is where you were. It does not get the last word.",
        "me_too": (
            "Maybe you have sat in the dark staring at the tile, wondering how "
            "life got here. I know that floor. You do not have to explain it "
            "to be allowed to stay and breathe."
        ),
        "scripture": {
            "reference": "Psalm 34:18",
            "translation": TRANSLATION,
            "text": (
                "The LORD is near to the brokenhearted and saves the crushed "
                "in spirit."
            ),
        },
        "teaching": (
            "David wrote this psalm after a frightening escape. The Hebrew "
            "word behind 'brokenhearted' comes from shabar, 'to break.' The "
            "verse says the LORD is near to people in exactly that state. It "
            "does not say the pain is a test you failed, and it does not say "
            "the pain disappears on a schedule."
        ),
        "application": (
            "You can tell God the truth before you know how to clean it up. "
            "Nearness is not the same as instant relief, so take the next "
            "small step toward help too."
        ),
        "soft_action": (
            "Grounding, your choice: feel your feet on the floor, or hold "
            "something cool, or name three things you can see. Eyes open is "
            "fine. Skip it if it does not help. Then say one honest sentence "
            "to God, or text one safe person."
        ),
        "safety_note": (
            "If you are thinking about hurting yourself or ending your life, "
            "call or text 988 now. Reaching out is not weak faith."
        ),
        "image_prompt": (
            "Adult coloring page, thick clean black outlines on a pure white "
            "background. A cracked tile floor with large, detailed wild roses "
            "growing up through the cracks. Fully closed line shapes, no gray "
            "shading, no gradients. --ar 11:14"
        ),
        "image_label": "symbolism",
    },
    2: {
        "title": "The Counterfeit Re-Up",
        "hook": "Some hungers do not get fed by what keeps promising to feed them.",
        "me_too": (
            "I know the chase: the next rush, the next bit of validation, "
            "another lap just to feel numb for a minute. I also know what it "
            "costs when the lap ends."
        ),
        "scripture": {
            "reference": "Isaiah 55:1-2",
            "translation": TRANSLATION,
            "text": (
                "Why do you spend your money for that which is not bread, and "
                "your labor for that which does not satisfy? Listen "
                "diligently to me, and eat what is good, and delight "
                "yourselves in rich food."
            ),
        },
        "teaching": (
            "God is speaking to exiles who have worn themselves out on things "
            "that do not feed them, and the invitation is free: come and "
            "eat. The passage is about turning back to God. It is not "
            "specifically about drugs or relationships, and it is not a "
            "judgment on anyone who is still struggling."
        ),
        "application": (
            "Honest accounting: what am I spending myself on that is not "
            "feeding me? Understanding why you reached for it is not "
            "excusing it, and a relapse does not make you disposable. "
            "Rebuilding takes support, and for addiction that can include "
            "treatment, a recovery group, and a doctor, not prayer alone."
        ),
        "soft_action": (
            "Write down your top three triggers. Next to each, write one "
            "person or place you can reach instead. Put the list somewhere "
            "you will see it. If you have a sponsor, counselor, or "
            "hotline number, add it."
        ),
        "safety_note": (
            "Stopping some substances suddenly can be medically dangerous. "
            "Talk to a doctor or call SAMHSA at 1-800-662-4357 before "
            "quitting on your own."
        ),
        "image_prompt": (
            "Adult coloring page, bold black ink outlines on pure white. A "
            "large ornate vintage hourglass; the top holds rough, jagged "
            "stones and, as they pass through the narrow middle, they "
            "become simple five-point stars falling into an open hand. "
            "Clean closed shapes, wide margins, no gray fills. --ar 11:14"
        ),
        "image_label": "symbolism",
    },
    3: {
        "title": "Control Is Not Love",
        "hook": "If you had to shrink to keep the peace, that was not peace.",
        "me_too": (
            "I know what it is to stay in something for years, hoping the "
            "change would come, absorbing the hits to keep things calm. "
            "Staying does not make you foolish. It makes you someone who was "
            "surviving."
        ),
        "scripture": {
            "reference": "Galatians 5:1",
            "translation": TRANSLATION,
            "text": (
                "For freedom Christ has set us free; stand firm therefore, "
                "and do not submit again to a yoke of slavery."
            ),
        },
        "teaching": (
            "Paul is writing to churches pressured to go back under the "
            "law as a requirement for belonging. The passage is about "
            "freedom in Christ. It does not speak directly about abusive "
            "relationships."
        ),
        "application": (
            "This is my application, not the text's subject: a life "
            "organized around fear and control is not the life Christ "
            "frees people for. Forgiveness does not require restored "
            "access, and leaving abuse is rarely easy or quick. Safety "
            "comes first."
        ),
        "soft_action": (
            "Do not make big moves alone or all at once. Today, only this: "
            "write down one trusted person and one hotline number. If you "
            "are still with someone controlling, do not block, confront, or "
            "announce anything until you have talked to an advocate about a "
            "safety plan, because leaving is often the most dangerous "
            "time. A letter to your past self is optional and can wait."
        ),
        "safety_note": (
            "National Domestic Violence Hotline: 1-800-799-7233, or text "
            "START to 88788. If a device may be monitored, use a safe one. "
            "Human trafficking help: 1-888-373-7888. In danger now: 911."
        ),
        "image_prompt": (
            "Adult coloring page, thick uniform black outlines on pure "
            "white. A woman's silhouette standing tall with open padlocks "
            "and a broken chain at her feet, and doves rising toward a "
            "radiant sun. Clean closed lines, no gray shading. --ar 11:14"
        ),
        "image_label": "symbolism",
    },
    4: {
        "title": "The Quiet Loop",
        "hook": "Not every loud thought in your head deserves to be believed.",
        "me_too": (
            "I know the background voice that says you are damaged, everyone "
            "leaves, and you will always fail. It can sound just like you."
        ),
        "scripture": {
            "reference": "John 10:10",
            "translation": TRANSLATION,
            "text": (
                "The thief comes only to steal and kill and destroy. I came "
                "that they may have life and have it abundantly."
            ),
        },
        "teaching": (
            "In context, Jesus is the good shepherd, and the 'thief' is "
            "contrasted with the shepherd who cares for the sheep. "
            "He came to give abundant life. The verse does not teach that "
            "every harsh thought is demonic."
        ),
        "application": (
            "Harsh self-talk can come from trauma, anxiety, exhaustion, "
            "depression, or old messages. We do not have to diagnose the "
            "source to answer it. We can test the thought against what "
            "Jesus says about us, and tell a safe person or a counselor "
            "when the loop will not quiet down."
        ),
        "soft_action": (
            "Thought check: (1) Notice it. (2) Say, 'That is a thought, "
            "not a fact.' (3) Ask, 'What would I say to a friend who "
            "believed this?' (4) Tell one safe person if it keeps coming "
            "back. Repeat as often as needed."
        ),
        "safety_note": (
            "If the thoughts include harming yourself, call or text 988."
        ),
        "image_prompt": (
            "Adult coloring page, deep black clean lines on pure white. A "
            "vintage microphone wrapped in barbed wire, with simple musical "
            "notes and light rays breaking through the wire. Closed lines, "
            "no gray fills. --ar 11:14"
        ),
        "image_label": "symbolism",
    },
    5: {
        "title": "Vineyard Work",
        "hook": "Pruning and loss can look alike. Only one of them is a lesson.",
        "me_too": (
            "I have lost friends, places, and plans, and I did not always "
            "know whether I was being protected or just hurt. I am still "
            "sorting some of it out."
        ),
        "scripture": {
            "reference": "John 15:1-2",
            "translation": TRANSLATION,
            "text": (
                "I am the true vine, and my Father is the vinedresser. Every "
                "branch of mine that does not bear fruit he takes away, and "
                "every branch that does bear fruit he prunes, that it may "
                "bear more fruit."
            ),
        },
        "teaching": (
            "Jesus is talking to his disciples about staying connected "
            "to him. The Greek for 'prunes' is kathairo, which also means "
            "'to cleanse.' The point of pruning is more fruit, "
            "through remaining in Christ."
        ),
        "application": (
            "This is interpretation: not everything you lost was God's "
            "pruning, and some losses are just grief that deserves to be "
            "grieved. We can ask what needs tending now, what we are "
            "carrying that no longer helps, and who can help us tend it. "
            "Fruit takes time, and nothing here promises a particular "
            "outcome."
        ),
        "soft_action": (
            "Make two short lists. 'I am grieving': what I lost. "
            "'I am tending': one small thing I can do this week to take "
            "care of myself or my future. Pick one item from the second "
            "list and put it on your calendar."
        ),
        "safety_note": "",
        "image_prompt": (
            "Adult coloring page, thick crisp black outlines on pure white. "
            "A thriving grapevine winding around a weathered wooden cross, "
            "heavy clusters of grapes, with dew drops drawn as simple open "
            "circles. No shading lines. --ar 11:14"
        ),
        "image_label": "symbolism",
    },
}


def build_blueprint():
    output_path = os.path.join(os.getcwd(), "devotional_blueprint.json")
    payload = {
        "brand": BRAND,
        "translation": TRANSLATION,
        "disclaimer": DISCLAIMER,
        "days": DEVOTIONAL_MATRIX,
    }
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
    except OSError as err:
        print(f"Could not write {output_path}: {err}")
        return 1
    print(f"Wrote {len(DEVOTIONAL_MATRIX)} days to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(build_blueprint())
