import glob
import os

import fiftyone as fo
import fiftyone.zoo as foz

images_patt = "../images/flower_photos/*/*"

# Create samples for your data
samples = []
for filepath in glob.glob(images_patt):
    sample = fo.Sample(filepath=filepath)

    # Store classification in a field name of your choice
    label = os.path.basename(os.path.dirname(filepath))
    sample["ground_truth"] = fo.Classification(label=label)

    samples.append(sample)

# Create dataset
dataset = fo.Dataset("flowers-dataset")
dataset.add_samples(samples)

session = fo.launch_app(dataset)
session.wait()