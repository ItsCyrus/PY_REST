class Item:
    def __init__(self, model, specs, color, availability, image):
        self.model = model
        self.specs = specs
        self.color = color
        self.availability = availability
        self.image = image

    def serialize(self):
        return {
            'model': self.model,
            'specs': self.specs,
            'color': self.color,
            'availability': self.availability,
            'image': self.image
        }
