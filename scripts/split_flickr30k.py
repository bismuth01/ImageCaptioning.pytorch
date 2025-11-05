import os
import json
import shutil
import argparse
from collections import Counter

def main(args):

    # Resolve paths
    json_file = os.path.expanduser(args.json_file)
    source_images_dir = os.path.expanduser(args.source_images_dir)
    output_base_dir = os.path.expanduser(args.output_base_dir)

    # Output directories
    train_dir = os.path.join(output_base_dir, "train")
    val_dir = os.path.join(output_base_dir, "val")
    test_dir = os.path.join(output_base_dir, "test")

    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    print("Reading JSON file...")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    images_data = data['images']
    print(f"Total images in JSON: {len(images_data)}")

    split_counter = Counter()
    copied_counter = Counter()
    missing_images = []
    errors = []

    print("\nProcessing images...")
    for idx, img_entry in enumerate(images_data):
        filename = img_entry['filename']
        split = img_entry['split']

        split_counter[split] += 1

        if split == "train":
            dest_dir = train_dir
        elif split in ["val", "validation"]:
            dest_dir = val_dir
        elif split == "test":
            dest_dir = test_dir
        else:
            errors.append(f"Unknown split '{split}' for {filename}")
            continue

        source_path = os.path.join(source_images_dir, filename)
        dest_path = os.path.join(dest_dir, filename)

        if os.path.exists(source_path):
            try:
                shutil.copy2(source_path, dest_path)
                copied_counter[split] += 1
            except Exception as e:
                errors.append(f"Error copying {filename}: {str(e)}")
        else:
            missing_images.append(filename)

        if (idx + 1) % 1000 == 0:
            print(f"  Processed {idx + 1}/{len(images_data)} images...")

    # Summary
    print(f"  Finished processing {len(images_data)} images.")
    print("\n========================")
    print("\nImages by split:", dict(split_counter))
    print("Copied:", dict(copied_counter))

    print(f"\nMissing images: {len(missing_images)}")
    if missing_images:
        print("Example:", missing_images[:5])

    success_rate = (sum(copied_counter.values()) / len(images_data) * 100)
    print(f"\nSuccess Rate: {success_rate:.2f}%")

    print("\nOutput directories:")
    print(train_dir)
    print(val_dir)
    print(test_dir)

    print("\n Done")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split Flickr30k dataset into train/val/test folders.")

    parser.add_argument("--json_file", default="~/dataset_flickr30k.json",
                        help="Path to dataset JSON file")
    parser.add_argument("--source_images_dir", default="~/Images/flickr30k_images",
                        help="Directory containing all Flickr30k images")
    parser.add_argument("--output_base_dir", default="~/dataset",
                        help="Output base directory where train/val/test folders are created")

    args = parser.parse_args()
    main(args)
