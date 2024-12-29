from graphics_engine.image_processing import ImageProcessing
from graphics_engine.construction_manager import ConstructionManager
from graphics_engine.algebric_processing import AlgebricProcessing
class GraphicsEngine:

    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.processor = ImageProcessing(self.working_dir)
        self.construction = ConstructionManager(self.working_dir)
        self.algebra = AlgebricProcessing(head_diameter=50)
    #   RUN EDGE DETECTION 
    def run_edge_detection(self, target):
        self.processor.optimize_for_extraction(target)

    def run_canny_edge_detection(self, image):
        return self.processor.run_canny_edge_detection(image)
    
    #   PLOTING TO CANVAS 
    def run_plotting_sequence(self, image):
        self.processor.run_plot_detection(image)

    #   RUNNING LOOMIS PLOT 
    def run_loomis_generation(self):
        self.construction.loomis_generation()

    def run_female_loomis(self):
        self.construction.generate_default_female()

    def run_alegbra(self, chin_start, chin_end):
        self.algebra.buildBaseForProfile2D(chin_start=chin_start, chin_end=chin_end)