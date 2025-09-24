import sys
from PIL import Image, ImageFilter
import os
# from sys import argv


def is_file_size_under_limit(file_path, size_limit_kb):
            file_size = os.path.getsize(file_path)  # Get size in bytes
            file_size_kb = file_size / 1024  # Convert to kilobytes
            return file_size_kb <= size_limit_kb

def save_image(edit, imgOutputPath, qualityNo):
    edit.save(imgOutputPath, quality=qualityNo)
            

if __name__ == '__main__':
    
    try:
        # link_input= argv[1]
        pathIn= input("Enter Images Directory Source Path: ")
        pathOut= input("Enter Images Directory Output Path: ")
        fileOutputFormat= input("Enter your desired output file format: ")
        desired_width= input("Enter your desired width for all image (Optional): ")

        size_kb_limit= input("Enter your desired size in kb for all image (Optional, default 100kb): ")
        size_kb_limit= 100 if size_kb_limit.strip() == "" else int(size_kb_limit.strip())

        for filename in os.listdir(pathIn):
            full_path = os.path.join(pathIn, filename)
            
            if os.path.isdir(full_path)== False:
                print("Processing: " + filename)
                img= Image.open(f"{pathIn}/{filename}")
                
                edit= img.filter(ImageFilter.SHARPEN)
                
                # Get the original dimensions
                original_width, original_height = img.size
                
                # if (original_width > 1000):
                try:    
                    desired_width= int(desired_width)
                
                    # Calculate the new height based on the desired width
                    new_height = int((desired_width / original_width ) * original_height)
                
                    resized_image= img.resize((desired_width, new_height), Image.LANCZOS)
                    edit= resized_image.filter(ImageFilter.SHARPEN)
                    
                except:  
                    pass
                
                
                clean_name= os.path.splitext(filename)[0]
                
                imgOutputPath= f"{pathOut}/{clean_name}.{fileOutputFormat}"
                
                initialQuality= 100
                save_image(edit, imgOutputPath, initialQuality)
                
                while is_file_size_under_limit(imgOutputPath, size_kb_limit) == False:
                    initialQuality -= 15
                    save_image(edit, imgOutputPath, initialQuality)
                        
                print("Processing Completed for " + filename + "\n")
            
        print("All Completed!!!")
        sys.exit(0)
    
    
    except Exception as e:
        sys.stderr.write("Error: " + str(e))
        sys.exit(1)