import pygame
import sys
import os

# تنظیمات برای موبایل
os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

# تنظیمات صفحه - برای موبایل مناسب‌تر
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mobile Game")

# رنگ‌ها
BACKGROUND = (240, 240, 240)
WHITE = (255, 255, 255)
BLUE = (30, 144, 255)
RED = (255, 59, 48)
GREEN = (52, 199, 89)
GRAY = (200, 200, 200)

# زمین بازی
ground_height = 50
ground_rect = pygame.Rect(0, SCREEN_HEIGHT - ground_height, SCREEN_WIDTH, ground_height)

# بازیکن
player_size = 50
player_rect = pygame.Rect(100, SCREEN_HEIGHT - ground_height - player_size, player_size, player_size)
player_speed = 5

# دکمه‌های کنترل در سمت راست پایین
button_size = 60
button_padding = 20
right_bottom_x = SCREEN_WIDTH - button_size - button_padding
right_bottom_y = SCREEN_HEIGHT - button_size - button_padding

# دکمه‌ها
buttons = {
    "left": {
        "rect": pygame.Rect(right_bottom_x - button_size - 10, right_bottom_y, button_size, button_size),
        "color": GREEN,
        "text": "←",
        "pressed": False
    },
    "jump": {
        "rect": pygame.Rect(right_bottom_x, right_bottom_y - button_size - 10, button_size, button_size),
        "color": RED,
        "text": "↑",
        "pressed": False
    },
    "right": {
        "rect": pygame.Rect(right_bottom_x + button_size + 10, right_bottom_y, button_size, button_size),
        "color": GREEN,
        "text": "→",
        "pressed": False
    }
}

# فونت - استفاده از فونت پیش‌فرض برای سازگاری بهتر
try:
    font = pygame.font.SysFont("Arial", 36, bold=True)
except:
    font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()

# متغیرهای پرش
is_jumping = False
jump_count = 10
original_y = player_rect.y


def handle_jump():
    global is_jumping, jump_count, original_y

    if is_jumping:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            player_rect.y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = 10
            player_rect.y = original_y


def main():
    global is_jumping, jump_count, original_y

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # هندل کردن رویدادهای لمسی
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                for button_name, button in buttons.items():
                    if button["rect"].collidepoint(mouse_pos):
                        button["pressed"] = True

                        if button_name == "jump" and not is_jumping:
                            is_jumping = True
                            original_y = player_rect.y

            if event.type == pygame.MOUSEBUTTONUP:
                for button in buttons.values():
                    button["pressed"] = False

        # حرکت مداوم وقتی دکمه نگه داشته شده است
        if buttons["left"]["pressed"]:
            player_rect.x -= player_speed
        if buttons["right"]["pressed"]:
            player_rect.x += player_speed

        # مدیریت پرش
        handle_jump()

        # محدودیت حرکت
        player_rect.x = max(0, min(player_rect.x, SCREEN_WIDTH - player_size))
        if not is_jumping:
            player_rect.y = min(player_rect.y, SCREEN_HEIGHT - ground_height - player_size)

        # رسم
        screen.fill(BACKGROUND)

        # زمین
        pygame.draw.rect(screen, GREEN, ground_rect)

        # بازیکن
        pygame.draw.rect(screen, BLUE, player_rect)

        # دکمه‌ها
        for button in buttons.values():
            # تغییر رنگ وقتی دکمه فشرده است
            color = button["color"]
            if button["pressed"]:
                color = (min(color[0] + 40, 255), min(color[1] + 40, 255), min(color[2] + 40, 255))

            # دایره دکمه
            pygame.draw.circle(screen, color, button["rect"].center, button_size // 2)
            pygame.draw.circle(screen, WHITE, button["rect"].center, button_size // 2 - 3)

            # متن دکمه
            text = font.render(button["text"], True, color)
            text_rect = text.get_rect(center=button["rect"].center)
            screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()