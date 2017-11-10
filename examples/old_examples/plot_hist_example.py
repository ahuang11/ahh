from ahh import vis, sci

scores = [99., 96., 94., 92., 86., 84., 82, 81, 80, 88., 94., 95., 90, 90, 90, 85, 83, 82, 81, 85, 75, 74, 54, 100]
stats = sci.get_stats(scores)
ax = vis.plot_bar(y=scores, title='Score Histogram', ylabel='Count', xlabel='Score', hist=True)
vis.set_axtext(ax, stats, loc='upper left')
vis.savefig('./example_images/scores_hist.png', close=True)

colors = ['blue', 'yellow', 'yellow', 'yellow', 'orange', 'red', 'green', 'red', 'yellow', 'green', 'green', 'orange']
ax = vis.plot_bar(x='text', y=colors, save='./example_images/colors_hist.png', color=vis.COLORS['blue'],
                  title='Color Histogram', ylabel='Count', xlabel='Colors', hist=True)
