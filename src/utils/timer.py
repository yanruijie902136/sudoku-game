import pygame
from pygame.locals import MOUSEBUTTONUP, QUIT


class Timer(pygame.sprite.Sprite):
    """
    Timer that starts counting up upon initialization.
    """

    def __init__(
        self,
        size: tuple[int, int],
        **kwargs,
    ) -> None:
        pygame.sprite.Sprite.__init__(self)

        # A subclass of Sprite should assign `image` and `rect` attributes.
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(**kwargs)

        self.font = pygame.font.SysFont("Futura", size=30)
        self.__start_time = pygame.time.get_ticks()

    def update(self) -> None:
        self.image.fill("white")
        pygame.draw.rect(self.image, "black",
                         ((0, 0), self.rect.size), width=3)

        text = self.font.render(self.get_elapsed_time(), True, "black")
        text_rect = text.get_rect(center=self.image.get_rect().center)
        self.image.blit(text, text_rect)

    def get_elapsed_time(self) -> str:
        """
        Get the elapsed time in "HH:MM:SS" format.
        """
        milliseconds = pygame.time.get_ticks() - self.__start_time
        hours, seconds = divmod(milliseconds // 1000, 3600)
        minutes, seconds = divmod(seconds, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def reset(self) -> None:
        """
        Reset the timer.
        """
        self.__start_time = pygame.time.get_ticks()


def main() -> None:
    """
    Simple test for Timer class.
    """
    pygame.init()
    pygame.display.set_caption("Timer Test")
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    timer = Timer(size=(250, 100), center=screen.get_rect().center)
    all_sprites = pygame.sprite.RenderPlain(timer)

    while True:
        clock.tick(60)

        screen.fill("white")
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                return

            if event.type == MOUSEBUTTONUP:
                # Reset the timer whenever user clicks mouse.
                timer.reset()


if __name__ == "__main__":
    main()
