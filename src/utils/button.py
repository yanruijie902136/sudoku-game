import pygame
from pygame.locals import QUIT


class Button(pygame.sprite.Sprite):
    """
    Rectangular button that inverts colors when the mouse is hovering over it.

    All buttons are black and white, and use Futura system font with size 30 to
    display their texts (subject to change).
    """

    def __init__(
        self,
        text: str,
        size: tuple[int, int],
        bg_color: str = "white",
        fg_color: str = "black",
        **kwargs,
    ) -> None:
        pygame.sprite.Sprite.__init__(self)

        # A subclass of Sprite should assign `image` and `rect` attributes.
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(**kwargs)

        self.text = text
        self.font = pygame.font.SysFont("Futura", size=30)
        self.bg_color = bg_color
        self.fg_color = fg_color

    def update(self) -> None:
        if self.is_hovered():
            self.image.fill(self.fg_color)
            text_color = self.bg_color
        else:
            self.image.fill(self.bg_color)
            pygame.draw.rect(self.image, self.fg_color,
                             ((0, 0), self.rect.size), width=3)
            text_color = self.fg_color

        text = self.font.render(self.text, True, text_color)
        text_rect = text.get_rect(center=self.image.get_rect().center)
        self.image.blit(text, text_rect)

    def is_hovered(self) -> bool:
        """
        Whether the mouse is hovering over the button.
        """
        return self.rect.collidepoint(pygame.mouse.get_pos())


def main() -> None:
    """
    Simple test for Button class.
    """
    pygame.init()
    pygame.display.set_caption("Button Test")
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    button = Button("BUTTON", size=(250, 100), center=screen.get_rect().center)
    all_sprites = pygame.sprite.RenderPlain(button)

    while True:
        clock.tick(60)

        screen.fill("white")
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                return


if __name__ == "__main__":
    main()
