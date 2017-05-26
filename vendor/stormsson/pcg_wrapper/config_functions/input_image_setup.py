import os
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import procedural_city_generation

class ImageSetup():

    def __init__(self, temp_dir_path):
        self.temp_dir_path = temp_dir_path

    def getImages(self,rule_image_path, density_image_path):
        '''
        Loads the rule-image and population-density-image from the filesystem.
        Saves the density image in /temp/ folder so that it could be ensured.

        Parameters
        ----------
        rule_image_name: String
            Name of the rule_image specified in Parameters
        density_image_name: String
            Name of the density_image specified in Parameters

        Returns
        --------
        rule_img: np.ndarray
            Rule-image as numpy array
        density_img: np.ndarray
            Density-image as numpy array
        '''

        #TODO: Document

        rule_img = mpimg.imread(rule_image_path)
        density_img = mpimg.imread(density_image_path)

        density_image_name = os.path.basename(density_image_path)


        plt.imsave(self.temp_dir_path+"/"+density_image_name.split(".")[0]+"diffused.png", density_img, cmap='gray')
        with open(self.temp_dir_path+"/"+density_image_name.split(".")[0]+"isdiffused.txt", 'w') as f:
            f.write("False")


        rule_img*=255
        density_img*=255
        return rule_img, density_img
