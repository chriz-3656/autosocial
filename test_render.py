from src.autosocial.renderers.pillow_paper_notes import PillowPaperNotesRenderer

renderer = PillowPaperNotesRenderer(output_dir="/tmp/autosocial_real")
print("Rendering symbol...")
renderer.render_image("A short one", "autosocial")
print("Rendering highlight...")
renderer.render_image("This is a medium length quote that gets highlighted", "autosocial")
print("Rendering statement...")
renderer.render_image("A very important statement — With a subtitle", "autosocial")
print("Rendering diagonal...")
renderer.render_image("This is an extremely long quote that forces the layout engine to jump straight to the diagonal layout because it is longer than seventy-five characters long.", "autosocial")
print("Done!")
