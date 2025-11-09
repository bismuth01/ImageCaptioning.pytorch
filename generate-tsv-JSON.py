import os
import json
import argparse

def process_folder(folder_path):
    """Process images from a folder and return list of image entries"""
    images_list = []
    
    if not os.path.exists(folder_path):
        print(f"Warning: Folder {folder_path} does not exist, skipping...")
        return images_list
    
    for filename in os.listdir(folder_path):
        # Skip if not an image file
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            continue
        
        # Extract image ID from filename (remove extension)
        try:
            img_id = int(os.path.splitext(filename)[0])
        except ValueError:
            # If filename is not a number, use hash or skip
            print(f"Warning: Cannot extract numeric ID from {filename}, skipping...")
            continue
        
        # Create image entry
        image_entry = {
            "id": img_id,
            "file_name": filename
        }
        
        images_list.append(image_entry)
    
    return images_list

def main():
    parser = argparse.ArgumentParser(description='Generate JSON file with image IDs and filenames')
    
    parser.add_argument('--train_dir', type=str, default='./flickr30k/train',
                        help='Path to train images directory (default: ./flickr30k/train)')
    parser.add_argument('--val_dir', type=str, default='./flickr30k/validation',
                        help='Path to validation images directory (default: ./flickr30k/validation)')
    parser.add_argument('--test_dir', type=str, default='./flickr30k/test',
                        help='Path to test images directory (default: ./flickr30k/test)')
    parser.add_argument('--output', '-o', type=str, default='./images_list.json',
                        help='Output JSON file path (default: ./images_list.json)')
    parser.add_argument('--skip_train', action='store_true',
                        help='Skip processing train images')
    parser.add_argument('--skip_val', action='store_true',
                        help='Skip processing validation images')
    parser.add_argument('--skip_test', action='store_true',
                        help='Skip processing test images')
    
    args = parser.parse_args()
    
    all_images = []
    
    # Process train images
    if not args.skip_train:
        print(f"Processing train images from {args.train_dir}...")
        train_images = process_folder(args.train_dir)
        print(f"  Found {len(train_images)} images")
        all_images.extend(train_images)
    else:
        print("Skipping train images")
        train_images = []
    
    # Process validation images
    if not args.skip_val:
        print(f"Processing validation images from {args.val_dir}...")
        val_images = process_folder(args.val_dir)
        print(f"  Found {len(val_images)} images")
        all_images.extend(val_images)
    else:
        print("Skipping validation images")
        val_images = []
    
    # Process test images
    if not args.skip_test:
        print(f"Processing test images from {args.test_dir}...")
        test_images = process_folder(args.test_dir)
        print(f"  Found {len(test_images)} images")
        all_images.extend(test_images)
    else:
        print("Skipping test images")
        test_images = []
    
    print(f"\nTotal images: {len(all_images)}")
    
    # Sort by ID for consistency
    all_images.sort(key=lambda x: x['id'])
    
    # Create final output
    output = {
        "images": all_images
    }
    
    print(f"\nSaving to {args.output}...")
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    
    print(f"Successfully created {args.output}")
    print(f"Total images: {len(all_images)}")
    if not args.skip_train:
        print(f"  - Train: {len(train_images)}")
    if not args.skip_val:
        print(f"  - Validation: {len(val_images)}")
    if not args.skip_test:
        print(f"  - Test: {len(test_images)}")
    
    print("\nDone!")

if __name__ == "__main__":
    main()