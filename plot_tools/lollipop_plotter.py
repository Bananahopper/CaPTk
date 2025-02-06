import matplotlib.pyplot as plt
import pandas as pd
import argparse
from matplotlib.font_manager import FontProperties


class LollipopPlotter:
    def __init__(self, datasets: list, names: list, save_path: str) -> None:
        self.datasets = datasets
        self.names = names
        self.save_path = save_path

    def process(self) -> None:
        for name, dataset in zip(self.names, self.datasets):
            self.access_data_and_plot(dataset, name)

    def access_data_and_plot(self, data_path: str, name: str) -> None:
        print(data_path)
        df = pd.read_csv(data_path, index_col=0)
        df = df.drop(index="void", errors='ignore')
        df.index = df.index.map(lambda x: 
            "Temporal Region" if "temporal" in x.lower() else 
            ("Frontal Region" if "frontal" in x.lower() else 
            ("Occipital Region" if "occipital" in x.lower() else x))
        )
        df = df.groupby(df.index).sum()
        ordered_df = df.sort_values(by="Tumor in region", ascending=False)
        x_range = range(0, len(df.index))

        # Make the plot
        plt.figure(figsize=(36, 10))
        plt.hlines(y=x_range, xmin=0, xmax=ordered_df["Tumor in region"], color="#FF6347")
        plt.plot(ordered_df["Tumor in region"], x_range, "o", c="#9932CC")

        # Add value labels at the end of each bar
        offset = 0.05
        for i, value in enumerate(ordered_df["Tumor in region"]):
            plt.text(value + offset, i, f"{value:.2f}", va='center', ha='left', fontsize=13, color='black', weight='bold')

        # FontProperties for bold text
        bold_font = FontProperties(weight='bold')

        # Add titles and axis names
        plt.title(f"Regions affected by tumors in the {name} dataset", fontsize=18, weight='bold')
        plt.xlabel(f"Percentage of tumors affecting specific region in the {name} dataset", fontsize=18, labelpad=25, weight='bold')
        plt.ylabel(f"Locations affected by tumors in the {name} dataset", fontsize=15, labelpad=18, weight='bold')

        # Set y-tick labels, bold for specific regions
        ytick_labels = []
        for label in ordered_df.index:
            if label in ["Temporal Region", "Frontal Region", "Occipital Region"]:
                ytick_labels.append(label)
            else:
                ytick_labels.append(label)
        
        plt.yticks(x_range, ytick_labels)  # Set y-tick labels normally first

        # Manually set bold font for specific labels
        ax = plt.gca()  # Get current axis
        for label in ax.get_yticklabels():
            label.set_fontsize(13)
            if label.get_text() in ["Temporal Region", "Frontal Region", "Occipital Region"]:
                label.set_fontproperties(bold_font)
                label.set_fontsize(13)

        plt.xlim(0, 20)  # Set x-axis limit

        # Save the plot
        plt.savefig(self.save_path + f"/lollipop_plot_for_{name}.png")
        plt.close()

# RUN THE CODE

datasets = ["output_analysis/Brats-2023-SSA/per_dataset_dist/Brats-2023-SSA/cortical_stats.csv", "output_analysis/Brats2021_wTumor/per_dataset_dist/Brats2021_wTumor/cortical_stats.csv", "output_analysis/Burdenko-GBM-Progression/per_dataset_dist/Burdenko-GBM-Progression/cortical_stats.csv", "output_analysis/LGG-1p19qDeletion/per_dataset_dist/LGG-1p19qDeletion/cortical_stats.csv", "output_analysis/QIN/per_dataset_dist/QIN/cortical_stats.csv", "output_analysis/RHUH_GBM/per_dataset_dist/RHUH_GBM/cortical_stats.csv", "output_analysis/UCSF-PDGM-v3/per_dataset_dist/UCSF-PDGM-v3/cortical_stats.csv"]
names = ["BraTS-SSA", "BraTS2021", "Burdenko", "LGG-1pq19-Deletion", "QIN", "RHUH", "UCSF"]
save_path = "output_plots"


lpop = LollipopPlotter(datasets, names, save_path)
lpop.process()


# def main(datasets, names, save_path):
#     lpop = LollipopPlotter(datasets, names, save_path)
#     lpop.process()


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Plot the datasets as lollipop plots")
#     parser.add_argument(
#         "--dirs", type=list, required=True, help="Directory containing the data"
#     )
#     parser.add_argument(
#         "--names", type=list, required=True, help="Name of the dataset for saving"
#     )
#     parser.add_argument(
#         "--save_path", type=str, required=True, help="Path to save the output files"
#     )
#     args = parser.parse_args()

#     main(args.dirs, args.names, args.save_path)
