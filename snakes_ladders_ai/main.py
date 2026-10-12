"""Snakes & Ladders AI solver - run:  python main.py
Compares BFS, DFS and IDDFS, prints a table, saves figures and a demo video/GIF."""
import os, random, subprocess, sys
from board import Board
from solvers import bfs, dfs, iddfs
import visualize as viz

OUT = "output"


def random_game(board, rng):
    s, n = board.start, 0
    while s != board.goal:
        mv = board.moves(s)
        s = rng.choice(mv)[1]; n += 1
    return n


def main(make_video=True):
    os.makedirs(OUT, exist_ok=True)
    b = Board()
    results = [bfs(b), dfs(b), iddfs(b)]

    print(f"{'Algorithm':<8}{'Throws':>8}{'Nodes':>8}{'Frontier':>10}{'Time(ms)':>10}  Optimal?")
    opt = results[0].throws
    for r in results:
        print(f"{r.name:<8}{r.throws:>8}{r.nodes_expanded:>8}{r.max_frontier:>10}"
              f"{r.seconds*1000:>10.3f}  {'YES' if r.throws == opt else 'NO'}")
    print("\nBFS optimal path :", " -> ".join(map(str, results[0].path)))
    print("BFS dice rolls   :", results[0].rolls)
    print("DFS path (first 10):", results[1].path[:10], "...")

    viz.save_paths(b, results[:2], f"{OUT}/bfs_vs_dfs_paths.png")
    viz.save_bfs_levels(b, results[0], f"{OUT}/bfs_levels.png")
    viz.save_comparison(results, f"{OUT}/comparison.png")
    rng = random.Random(42)
    games = [random_game(b, rng) for _ in range(10000)]
    viz.save_histogram(games, opt, f"{OUT}/random_vs_bfs.png")
    print(f"Random play: mean {sum(games)/len(games):.1f} throws, best {min(games)}, worst {max(games)}")

    if make_video:
        frames = viz.make_frames(b, results[0], OUT)
        # GIF + MP4 from frames
        from PIL import Image
        imgs = [Image.open(f).convert("RGB") for f in frames]
        imgs[0].save(f"{OUT}/bfs_demo.gif", save_all=True, append_images=imgs[1:], duration=900, loop=0)
        try:
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", "frames/f%03d.png",
                            "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                            f"{OUT}/bfs_demo.mp4"], check=True)
        except Exception as e:
            print("ffmpeg not available, GIF only:", e)
    return results


if __name__ == "__main__":
    main(make_video="--no-video" not in sys.argv)
