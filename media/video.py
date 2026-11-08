"""Builds the narrated walkthrough (<= 5 min) from the rendered slides.
Narration numbers come from results/summary.json. Voice: edge-tts (en-US-AvaNeural, an AI voice; needs edge-tts >= 7.3.1, set EDGE_TTS to its path) and ffmpeg.
    python media/video.py            -> media/build/AeroMargin-walkthrough.mp4 (+ narration.txt)"""
import hashlib
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SL = ROOT / "docs" / "slides"
OUT = ROOT / "media" / "build"
OUT.mkdir(parents=True, exist_ok=True)
S = json.loads((ROOT / "results" / "summary.json").read_text(encoding="utf-8"))
p = lambda m: round(100 * S[m]["pass_rate"]) if m in S else 0
ph = lambda m: round(100 * S[m]["pass_hat_k"]) if m in S else 0

LINES = [
    "Hi, we're Paras and Harshita. This is AeroMargin: an eval of whether a language model picks the right method, and the right sign, before it calculates. "
    "Ten aerospace hand calculations: airframe stress, fatigue, loads, flight performance and weight and balance. Each one hides a single condition that reverses a textbook default.",
    "Engineers already ask chat models for this work. In a 2025 industry survey, seventy-nine percent of aerospace design engineers whose companies had not approved AI tools were using them anyway. "
    "And a wrong margin of safety looks exactly like a right one. Here, the textbook formula says plus zero point seven one, pass. A checker who draws the free body gets minus zero point zero eight, fail.",
    "Here are the ten tasks. An oblique-load lug that needs Bruhn's one-point-six power interaction. A short strut where the Johnson parabola governs, not Euler. True airspeed above the tropopause. "
    "A load sheet where the fuel arm moves. A fatigue life driven by the ground-air-ground cycle. A takeoff where the METAR wind is in degrees true and a NOTAM shortens the runway. "
    "Gust loads that are worst at light weight. A bolt group where the most loaded bolt is not the critical one. A tapered beam. And a Z-section in unsymmetric bending.",
    "Task nine shows the idea. Every textbook teaches the Resal relief: in a tapered beam, the inclined flanges carry part of the shear. But that only holds when the beam gets deeper toward the root. "
    "This beam is deeper at its free end. Draw the free body and both flange components point up, with the load. The web carries seven thousand eight hundred pounds, not four thousand two hundred. "
    "The familiar formula is unconservative by eighty-six percent, and it flips the verdict.",
    "Grading is code only, no language-model judge. Each task states every output and its JSON keys, and has a reference solution. Before any model ran, a validation script made one hundred thirty-three checks. "
    "The grader accepts the reference and reformatted versions of it, and tolerates rounding. It rejects every critical field pushed past tolerance, twenty-four trap answers built from specific engineering mistakes, "
    "and gaming attempts like echoed templates or hedged verdicts. We also read every failing transcript, and widened three tolerances where models were only rounding.",
    f"Results, three trials per task, same prompts and graders. At medium reasoning, the two newest frontier models, GPT five point six Sol and GPT five point five, pass every trial. "
    f"GPT five point four passes {p('gpt-5.4')} percent. Gemini three point five Flash, {p('gemini-3.5-flash')} percent. GPT five point four mini, {p('gpt-5.4-mini')} percent. "
    f"o3, the frontier reasoning model of 2025, passes {p('o3')} percent, and is right on all three trials for only {ph('o3')} percent of tasks. The open Gemma 4 model passes {p('gemma-4-31b')} percent.",
    f"The decisive variable is reasoning effort. Same model, same prompts. Turn reasoning off, the setting behind fast chat modes, and GPT five point six Sol drops to {p('gpt-5.6-sol-none')} percent, "
    f"and GPT five point five to {p('gpt-5.5-none')} percent. On the tapered beam, Sol without reasoning used the textbook relief formula on every trial. "
    "With reasoning on, both models also passed every sign-reversed variant we generated for tasks nine and ten, so those passes are real.",
    "The transcripts show the mechanism. o3 states, on all three trials, that Bruhn gives an elliptical interaction for lugs. It doesn't. So it passes a fitting that fails. "
    "Sol without reasoning applies the relief formula to a beam that tapers the other way. GPT five point five without reasoning reads the METAR wind as magnetic and gets two knots of headwind instead of five and a half.",
    "Our takeaway: the gap is not arithmetic. It's recall versus re-derive. The same model is right every time when it reasons, and confidently wrong when it answers from memory. "
    "For engineering teams, the reasoning setting matters more than the leaderboard. Ask the model for the governing case and the direction of every load before any number, the way a senior checker would. "
    "Everything is reproducible with three commands, and every transcript is in the repository. Thank you.",
]


def tts(text, path):
    exe = os.environ.get("EDGE_TTS", "edge-tts")   # edge-tts >= 7.3.1
    subprocess.run([exe, "--voice", "en-US-AvaNeural", "--rate", "+4%", "--text", text, "--write-media", str(path)], check=True)


def dur(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)]).decode().strip())


def main():
    (OUT / "narration.txt").write_text("\n\n".join(f"[Slide {i + 1}] {t}" for i, t in enumerate(LINES)), encoding="utf-8")
    parts = []
    for i, text in enumerate(LINES, 1):
        mp3 = OUT / f"line-{i}-{hashlib.sha1(text.encode()).hexdigest()[:8]}.mp3"   # re-voiced only when the text changes
        if not mp3.exists():
            tts(text, mp3)
        d = dur(mp3) + 0.8
        clip = OUT / f"clip-{i}.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", str(SL / f"s{i}.png"), "-i", str(mp3),
                        "-af", "apad=pad_dur=0.8", "-t", f"{d:.2f}", "-r", "30", "-c:v", "libx264", "-tune", "stillimage",
                        "-pix_fmt", "yuv420p", "-vf", "scale=1920:1080", "-c:a", "aac", "-b:a", "160k", str(clip)], check=True)
        parts.append(clip)
        print(f"slide {i}: {d:.1f}s")
    lst = OUT / "list.txt"
    lst.write_text("".join(f"file '{c.as_posix()}'\n" for c in parts), encoding="utf-8")
    final = OUT / "AeroMargin-walkthrough.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(final)], check=True)
    print("wrote", final, f"{dur(final):.0f}s")


if __name__ == "__main__":
    main()
