import pygame

class Sprite_sheet:
    """Handles srite loading from sprite sheet."""
    def __init__(self, sheet):
        self.sheet = sheet

    def get_image(self, frame, width, height, scale, color):
        """Gets specific sprite from sprite sheet and returns it as a sprite image."""
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)

        return image
    
    