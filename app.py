import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Create a new figure and axis
fig, ax = plt.subplots(figsize=(10, 6))


# Function to add a text box with an arrow
def add_box(ax, text, xy, width=1.8, height=1, text_offset=(0.5, 0.5)):
    rect = patches.FancyBboxPatch(
        (xy[0] - width / 2, xy[1] - height / 2),
        width,
        height,
        boxstyle="round,pad=0.3",
        edgecolor="black",
        facecolor="lightgrey",
    )
    ax.add_patch(rect)
    ax.text(xy[0], xy[1], text, ha="center", va="center", fontsize=10)


# Add client-side (browser) box
add_box(ax, "Browser\n(Client)", (1, 2.5))

# Add Flask server box
add_box(ax, "Flask Server", (4, 2.5))

# Add arrows to indicate flow
arrowprops = dict(facecolor="black", arrowstyle="->")

# Arrow from Browser to Flask Server
ax.annotate("", xy=(2.5, 2.5), xytext=(1.8, 2.5), arrowprops=arrowprops)
ax.text(2.15, 2.65, "Send URL", fontsize=9, ha="center")

# Arrow from Flask Server to Browser
ax.annotate("", xy=(1.8, 2), xytext=(2.5, 2), arrowprops=arrowprops)
ax.text(2.15, 1.85, "Receive Short URL", fontsize=9, ha="center")

# Set limits and remove axes
ax.set_xlim(0, 6)
ax.set_ylim(1, 4)
ax.axis("off")

# Display the diagram
plt.show()
