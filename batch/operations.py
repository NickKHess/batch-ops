import os
from os import path, listdir

class FindAndReplace():
    def __init__(self, directory, extension, find, replace, verbose=False):
        self.prefix = 'FindAndReplace'

        # ----- Error Checks -----

        # Verify that the dir is a directory
        if not path.isdir(directory):
            raise IOError(f'No such directory \'{directory}\'.')

        # Append a period to the extension if needed
        if not extension[0] == '.':
            extension = '.' + extension

        # ----- End Error Checks -----

        self.directory = directory
        self.extension = extension
        self.find = find
        self.replace = replace
        self.verbose = verbose

    def execute(self):
        # Files in the given folder with the given extension (excludes temp files generated by the module.
        files = [file for file in listdir(self.directory) if path.isfile(path.join(self.directory, file)) and (self.extension in file) and (not '-temp' + self.extension in file)]

        for file in files:
            no_ext = file.replace(self.extension, '')
            try:
                if self.verbose:
                    print(f'{self.prefix} is finding \'{self.find}\' and replacing it with \'{self.replace}\' in \'{file}\'')

                file_path = path.join(self.directory, file)

                # Open the file
                open_file = open(file_path, mode='r')

                temp_path = path.join(self.directory, f'{no_ext}-temp{self.extension}')
                temp = open(temp_path, mode='w')

                # Read the file, write to temp file
                text = open_file.readlines()
                i = 0
                for line in text:
                    text[i] = line.replace(self.find, self.replace)
                    temp.write(text[i])
                    i += 1

                # Close the files so they're not in use
                open_file.close()
                temp.close()

                # Remove the original file (to be overwritten)
                os.remove(file_path)
                # Overwrite
                os.rename(temp_path, file_path)
            except Exception as e:
                print(f'{self.prefix} could not access \'{file}\'. Skipping this file.')
            finally:
                # Close the files if they're not open
                if (not open_file.closed) and (not temp.closed):
                    open_file.close()
                    temp.close()

                # Clean up leftovers
                if path.exists(temp_path):
                    os.remove(temp_path)

        print(f'{self.prefix} operation complete in \'{self.directory}\'!')
