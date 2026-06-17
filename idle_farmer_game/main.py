import pygame
import tkinter
import math
import random
import sys
from pathlib import Path


def play_music():
    import pygame

    music_path = Path(__file__).with_name("background.mp3")
    if not music_path.exists():
        music_path = Path(__file__).with_name("assets") / "background.mp3"

    pygame.mixer.init()
    pygame.mixer.music.load(str(music_path))
    pygame.mixer.music.play(loops=-1)


level = 1
totalclicks = 0
levelpoints = 0
seeds = 20
potatoes = 0
farmers = 0
tools = 1
plantsperclick = 1 + tools
wheat = 0
corn = 0
storage = 1
maxStorage = 25 * storage
marketers = 0
plantspertick = 1000
money = 20
plantspersec = 0
sellpersec = 0

plantspersec_accumulator = 0
plantspersec_job_id = None
sellpersec_job_id = None
seed_auto_job_id = None

clicksneeded = 300 * level
prices = {
    "potatoes": int(3),
    "corn": int(5),
    "wheat": int(7)
}

root = None


def sell():
    global money, potatoes, corn, wheat, totalclicks, levelpoints, balance_label, crops_label
    totalclicks += 1
    levelpoints += 0.03

    available = []
    if potatoes > 0:
        available.append("potatoes")
    if corn > 0:
        available.append("corn")
    if wheat > 0:
        available.append("wheat")

    if not available:
        return False

    randcrop = random.choice(available)

    if randcrop == "potatoes":
        potatoes -= 1
    elif randcrop == "corn":
        corn -= 1
    else:
        wheat -= 1

    money += prices[randcrop]
    print(f"Sold 1 {randcrop}, +{prices[randcrop]} money (balance={money})")

    try:
        balance_label.config(text=f"Balance: {money}    Seeds: {seeds}   Storage: {maxStorage}")
    except Exception:
        pass
    try:
        crops_label.config(text=f"Potatoes: {potatoes} Corn: {corn} Wheat: {wheat}")
    except Exception:
        pass

    return True


def plant_potato():
    global levelpoints, totalclicks, potatoes, seeds, money, prices
    if seeds < 2:
        print("Not enough seeds to plant potato")
        return False
    levelpoints += 0.01
    totalclicks += 1
    potatothen = potatoes
    potatoes += random.choice([math.floor(1 * plantsperclick), math.floor(2 * plantsperclick), math.floor(3 * plantsperclick)])
    potatonow = potatoes
    seeds -= potatonow - potatothen - 1
    print(f"Level: {level}, Points: {levelpoints:.2f}, Clicks: {totalclicks}, Potatoes: {potatoes}")
    try:
        balance_label.config(text=f"Balance: {money}     Seeds: {seeds}     Storage: {maxStorage}")
    except Exception:
        pass
    return True


def plant_corn():
    global levelpoints, totalclicks, corn, seeds, money, prices
    if seeds < 2:
        print("Not enough seeds to plant corn")
        return False
    levelpoints += 0.01
    totalclicks += 1
    cornthen = corn
    corn += random.choice([math.floor(1 * plantsperclick), math.floor(2 * plantsperclick), math.floor(3 * plantsperclick)])
    cornnow = corn
    seeds -= cornnow - cornthen - 1
    print(f"Level: {level}, Points: {levelpoints:.2f}, Clicks: {totalclicks}, Corn: {corn}")
    try:
        balance_label.config(text=f"Balance: {money}     Seeds: {seeds}     Storage: {maxStorage}")
    except Exception:
        pass
    return True


def plant_wheat():
    global levelpoints, totalclicks, wheat, seeds, money, prices
    if seeds < 2:
        print("Not enough seeds to plant wheat")
        return False
    levelpoints += 0.01
    totalclicks += 1
    wheatthen = wheat
    wheat += random.choice([math.floor(1 * plantsperclick), math.floor(2 * plantsperclick), math.floor(3 * plantsperclick)])
    wheatnow = wheat
    seeds -= wheatnow - wheatthen - 1
    print(f"Level: {level}, Points: {levelpoints:.2f}, Clicks: {totalclicks}, Wheat: {wheat}")
    try:
        balance_label.config(text=f"Balance: {money}     Seeds: {seeds}     Storage: {maxStorage}")
    except Exception:
        pass
    return True


def seed():
    global money, seeds, totalclicks, levelpoints
    if money < 3:
        print("Not enough money to buy seeds")
        return False
    money -= 3
    seeds += 5
    totalclicks += 1
    levelpoints += 0.02
    print(f"Levelpoints={levelpoints:.2f}, Bought 5 seeds for 10 money (balance={money}), Seeds={seeds}")
    try:
        balance_label.config(text=f"Balance: {money}     Seeds: {seeds}     Storage: {maxStorage}")
    except Exception:
        pass
    return True


def addstorage():
    global money, storage, maxStorage, totalclicks, levelpoints
    cost = 10 * (level * 2)
    if money < cost:
        print("Not enough money to upgrade storage")
        return False
    totalclicks += 1
    levelpoints += 0.05
    storage += 1
    maxStorage = 25 * storage
    print(f"Levelpoints: {levelpoints}, Upgraded storage to {maxStorage} for {cost} money")
    money -= cost
    return True


def farmer():
    global money, farmers, plantspersec, totalclicks, levelpoints
    cost = 33 * level
    if money < cost:
        print("Not enough money to hire farmers")
        return False
    levelpoints += 0.03
    totalclicks += 1
    farmers += 1
    money -= cost
    return True


def marketer():
    global money, marketers, totalclicks, levelpoints, sellpersec, sellpersec_job_id, seed_auto_job_id, root
    cost = 40 * level
    if money < cost:
        print("Not enough money to hire marketers")
        return False
    levelpoints += 0.03
    totalclicks += 1
    marketers += 1
    money -= cost
    try:
        sellpersec = float(marketers)
    except Exception:
        sellpersec = marketers
    try:
        if sellpersec_job_id is None and root is not None:
            sellpersec_job_id = root.after(0, sellpersecond)
    except Exception:
        pass
    try:
        if seed_auto_job_id is None and root is not None:
            seed_auto_job_id = root.after(0, auto_buy_seeds)
    except Exception:
        pass
    return True


def tool():
    global money, tools, plantsperclick, totalclicks, levelpoints
    cost = 50 * (level * 0.5)
    if money < cost:
        print("Not enough money to upgrade tools")
        return False
    levelpoints += 0.04
    totalclicks += 1
    tools += 0.25
    plantsperclick += tools
    money -= cost
    return True


def setup_and_gui():
    global root, money, potatoes, corn, wheat, level, maxStorage, seeds
    global buttoncorn, buttonpotato, buttonwheat, buttonstorage, buttonsell, buttonseed, buttonfarmer
    global balance_label, crops_label, level_label
    root = tkinter.Tk()
    root.geometry("800x500")
    root.title("Farmer Game")

    top_frame = tkinter.Frame(root)
    top_frame.pack(side="top", fill="x")

    left_frame = tkinter.Frame(top_frame)
    left_frame.pack(side="left")
    center_frame = tkinter.Frame(top_frame)
    center_frame.pack(side="left", expand=True, fill="x")
    right_frame = tkinter.Frame(top_frame)
    right_frame.pack(side="right")
    topleft_row = tkinter.Frame(left_frame)
    topleft_row.pack(side="top")

    buttonstorage = tkinter.Button(topleft_row, text="Upgrade Storage", font=("Poor Richard", 12), command=addstorage)
    buttonstorage.pack(side="left", padx=6, pady=6)

    buttonfarmer = tkinter.Button(topleft_row, text="Hire Farmers", font=("Poor Richard", 12), command=farmer)
    buttonfarmer.pack(side="left", padx=6, pady=6)

    topleft2_row = tkinter.Frame(left_frame)
    topleft2_row.pack(side="top", anchor="w")

    buttontools = tkinter.Button(topleft2_row, text="Upgrade Tools", font=("Poor Richard", 12), command=tool)
    buttontools.pack(side="left", padx=6, pady=6)

    buttonmarketer = tkinter.Button(topleft2_row, text="Hire Marketers", font=("Poor Richard", 12), command=marketer)
    buttonmarketer.pack(side="left", padx=6, pady=6)

    center_buttons = tkinter.Frame(root)
    center_buttons.pack(pady=30)

    title_label = tkinter.Label(root, text="Farmer Game", font=("Poor Richard", 24))
    title_label.place(relx=0.5, y=10, anchor="n")

    balance_label = tkinter.Label(root, text=f"Balance: {money}   Seeds: {seeds}  Storage: {maxStorage}", font=("Poor Richard", 14))
    balance_label.pack(pady=8)

    crops_label = tkinter.Label(root, text=f"Potatoes: {potatoes} Corn: {corn} Wheat: {wheat}", font=("Poor Richard", 12))
    crops_label.pack(pady=10)

    buttoncorn = tkinter.Button(center_buttons, text="Plant Corn", font=("Poor Richard", 16), command=plant_corn)
    buttoncorn.pack(side="left", padx=12)
    buttoncorn.config(state="disabled")

    buttonpotato = tkinter.Button(center_buttons, text="Plant Potato", font=("Poor Richard", 16), command=plant_potato)
    buttonpotato.pack(side="left", padx=12)

    buttonwheat = tkinter.Button(center_buttons, text="Plant Wheat", font=("Poor Richard", 16), command=plant_wheat)
    buttonwheat.pack(side="left", padx=12)
    buttonwheat.config(state="disabled")

    level_label = tkinter.Label(right_frame, text=f"Level {level}", font=("Poor Richard", 16))
    level_label.pack(side="right", padx=6, pady=6)

    action_frame = tkinter.Frame(right_frame)
    action_frame.pack(side="top", padx=6, pady=6)

    buttonseed = tkinter.Button(action_frame, text="Buy Seeds", font=("Poor Richard", 12), command=seed)
    buttonseed.pack(side="left", padx=6)

    buttonsell = tkinter.Button(action_frame, text="Sell Crops", font=("Poor Richard", 12), command=sell)
    buttonsell.pack(side="left", padx=6)

    def update_buttons():
        global wheat, potatoes, corn, money, seeds, level, maxStorage
        root.after(200, update_buttons)
        try:
            level_label.config(text=f"Level {level}")
        except Exception:
            pass
        try:
            balance_label.config(text=f"Balance: {money}     Seeds: {seeds}     Storage: {maxStorage}")
        except Exception:
            pass
        try:
            crops_label.config(text=f"Potatoes: {potatoes} Corn: {corn} Wheat: {wheat}")
        except Exception:
            pass

        if level == 1:
            buttonpotato.config(state="normal")
            buttoncorn.config(state="disabled")
            buttonwheat.config(state="disabled")
            buttonsell.config(state="normal")
            buttonstorage.config(state="normal")
            buttontools.config(state="disabled")
            buttonfarmer.config(state="disabled")
            buttontools.config(state="disabled")

        if level >= 1:
            if money >= 10 * (level ** 2):
                buttonstorage.config(state="normal")
            if storage == level + 2:
                buttonstorage.config(state="disabled")
            if potatoes + corn + wheat == 0:
                buttonsell.config(state="disabled")

            if level >= 3:
                buttontools.config(state="normal")
            if seeds >= math.floor(3 * plantsperclick):
                buttonpotato.config(state="normal")
                if level >= 2:
                    buttoncorn.config(state="normal")
                if level >= 3:
                    buttonwheat.config(state="normal")
            if money < 10 * (level * 2):
                buttonstorage.config(state="disabled")
            if money >= 10 * (level * 2):
                buttonstorage.config(state="normal")
            if money < 33 * level:
                buttonfarmer.config(state="disabled")
            if money >= 33 * level:
                buttonfarmer.config(state="normal")
            if money <= 40 * level:
                buttonmarketer.config(state="disabled")
            if money >= 40 * level:
                buttonmarketer.config(state="normal")
            if potatoes + corn + wheat >= 1:
                buttonsell.config(state="normal")
            if money > 33 * level:
                buttonfarmer.config(state="disabled")
            if money <= 33 * level:
                if level >= 3:
                    buttonfarmer.config(state="normal")
            if money >= 50:
                if tools == 1:
                    buttontools.config(state="normal")
                elif money < 50 * (level * 0.5):
                    buttontools.config(state="disabled")
            if money <= 50 * (level * 0.5):
                buttonmarketer.config(state="disabled")
            if money >= 50 * (level * 0.5):
                buttonmarketer.config(state="normal")

        elif level == 2:
            buttonpotato.config(state="normal")
            buttoncorn.config(state="normal")
            buttonwheat.config(state="disabled")
            buttonstorage.config(state="normal")
            buttontools.config(state="normal")
            buttonfarmer.config(state="disabled")
            buttontools.config(state="normal")
            if money - 50 * (level * 0.5) < 0:
                buttontools.config(state="disabled")
            else:
                buttontools.config(state="normal")

        elif level == 3:
            buttonpotato.config(state="normal")
            buttoncorn.config(state="normal")
            buttonwheat.config(state="normal")
            buttonstorage.config(state="normal")
            buttontools.config(state="normal")
            buttonfarmer.config(state="disabled")
            buttonmarketer.config(state="disabled")
            buttontools.config(state="normal")
        elif level == 4:
            buttonpotato.config(state="normal")
            buttoncorn.config(state="normal")
            buttonwheat.config(state="normal")
            buttonstorage.config(state="normal")
            buttontools.config(state="normal")
            buttonfarmer.config(state="normal")
            buttonmarketer.config(state="disabled")
            buttontools.config(state="normal")
        elif level >= 5:
            buttonpotato.config(state="normal")
            buttoncorn.config(state="normal")
            buttonwheat.config(state="normal")
            buttonstorage.config(state="normal")
            buttontools.config(state="normal")
            buttonfarmer.config(state="normal")
            buttonmarketer.config(state="normal")
            buttontools.config(state="normal")
        try:
            total_crops = potatoes + corn + wheat
            if total_crops > 0:
                buttonsell.config(state="normal")
            else:
                buttonsell.config(state="disabled")
        except Exception:
            pass

        if corn >= maxStorage:
            buttoncorn.config(state="disabled")
            corn = maxStorage
        if wheat >= maxStorage:
            buttonwheat.config(state="disabled")
            wheat = maxStorage
        if potatoes >= maxStorage:
            buttonpotato.config(state="disabled")
            potatoes = maxStorage

        if money < 10:
            buttonseed.config(state="disabled")
        else:
            buttonseed.config(state="normal")

        if seeds <= 5:
            buttonpotato.config(state="disabled")
            buttoncorn.config(state="disabled")
            buttonwheat.config(state="disabled")

        if storage >= maxStorage:
            try:
                buttonstorage.pack_forget()
            except Exception:
                pass
        else:
            if not buttonstorage.winfo_ismapped():
                buttonstorage.pack(side="left", padx=6, pady=6)
    update_buttons()

    root.after(200, update_buttons)


def level_up():
    global level, levelpoints, maxStorage, clicksneeded, buttonstorage
    levelpoints = 0.0
    level += 1
    maxStorage += 5
    clicksneeded = level * 300
    try:
        if not buttonstorage.winfo_ismapped():
            buttonstorage.pack(side="left", padx=6, pady=6)
    except Exception:
        pass


def game_loop():
    global level, levelpoints, totalclicks, potatoes, corn, wheat
    if levelpoints >= 2 + (level * 2):
        level_up()
    if totalclicks >= clicksneeded:
        level_up()
    if storage >= maxStorage:
        try:
            buttonstorage.config(state="disabled")
        except Exception:
            pass
    if potatoes > maxStorage:
        potatoes = maxStorage
    if corn > maxStorage:
        corn = maxStorage
    if wheat > maxStorage:
        wheat = maxStorage

    root.after(200, game_loop)


def available_crops():
    try:
        choices = []
        if buttonpotato.cget("state") == "normal":
            choices.append("potatoes")
        if buttoncorn.cget("state") == "normal":
            choices.append("corn")
        if buttonwheat.cget("state") == "normal":
            choices.append("wheat")
        return choices
    except Exception:
        return ["potatoes", "corn", "wheat"]


def tick():
    global potatoes, corn, wheat, farmers, maxStorage, money, seeds

    choices = available_crops()

    if farmers > 0 and choices:
        for i in range(farmers):
            crop = random.choice(choices)
            if crop == "potatoes":
                potatoes = min(potatoes + 1, maxStorage)
            elif crop == "corn":
                corn = min(corn + 1, maxStorage)
            else:
                wheat = min(wheat + 1, maxStorage)

    try:
        balance_label.config(text=f"Balance: {money}     Seeds: {seeds}     Storage: {maxStorage}")
    except Exception:
        pass

    try:
        crops_label.config(text=f"Potatoes: {potatoes} Corn: {corn} Wheat: {wheat}")
    except Exception:
        pass

    try:
        root.after(1000, tick)
    except Exception:
        pass


def plantspersecond():
    global plantspersec_job_id, plantspersec, potatoes, corn, wheat, maxStorage

    try:
        rate = float(plantspersec)
    except Exception:
        rate = 0.0

    if rate <= 0:
        try:
            plantspersec_job_id = root.after(1000, plantspersecond)
        except Exception:
            pass
        return

    try:
        interval_ms = max(1, int(round(1000.0 / rate)))
    except Exception:
        interval_ms = 1000

    choices = available_crops()
    if not choices:
        try:
            plantspersec_job_id = root.after(1000, plantspersecond)
        except Exception:
            pass
        return

    crop = random.choice(choices)
    if crop == "potatoes":
        potatoes = min(potatoes + 1, maxStorage)
    elif crop == "corn":
        corn = min(corn + 1, maxStorage)
    else:
        wheat = min(wheat + 1, maxStorage)

    try:
        crops_label.config(text=f"Potatoes: {potatoes} Corn: {corn} Wheat: {wheat}")
    except Exception:
        pass

    try:
        plantspersec_job_id = root.after(interval_ms, plantspersecond)
    except Exception:
        pass


def sellpersecond():
    global sellpersec, money, sellpersec_job_id, potatoes, corn, wheat, maxStorage, seeds

    try:
        rate = float(sellpersec)
    except Exception:
        rate = 0.0

    if rate <= 0:
        try:
            sellpersec_job_id = root.after(1000, sellpersecond)
        except Exception:
            pass
        return

    try:
        interval_ms = max(1, int(round(1000.0 / rate)))
    except Exception:
        interval_ms = 1000

    total_crops = (potatoes or 0) + (corn or 0) + (wheat or 0)
    if total_crops <= 0:
        try:
            sellpersec_job_id = root.after(1000, sellpersecond)
        except Exception:
            pass
        return

    sold = sell()

    try:
        balance_label.config(text=f"Balance: {money}     Seeds: {seeds}     Storage: {maxStorage}")
    except Exception:
        pass
    try:
        crops_label.config(text=f"Potatoes: {potatoes} Corn: {corn} Wheat: {wheat}")
    except Exception:
        pass

    try:
        if sold:
            sellpersec_job_id = root.after(interval_ms, sellpersecond)
        else:
            sellpersec_job_id = root.after(1000, sellpersecond)
    except Exception:
        pass


def auto_buy_seeds():
    global money, seeds, totalclicks, levelpoints, balance_label, seed_auto_job_id, root, marketers
    try:
        if marketers <= 0:
            try:
                seed_auto_job_id = root.after(1000, auto_buy_seeds)
            except Exception:
                pass
            return

        qty = marketers * 2
        cost = marketers * 3

        if money < cost:
            try:
                seed_auto_job_id = root.after(1000, auto_buy_seeds)
            except Exception:
                pass
            return

        money -= cost
        seeds += qty
        totalclicks += 1
        levelpoints += 0.02 * marketers
        print(f"Auto-bought {qty} seeds for {cost} money (balance={money}), Seeds={seeds}")

        try:
            balance_label.config(text=f"Balance: {money}     Seeds: {seeds}     Storage: {maxStorage}")
        except Exception:
            pass

        try:
            seed_auto_job_id = root.after(2000, auto_buy_seeds)
        except Exception:
            pass
    except Exception:
        try:
            seed_auto_job_id = root.after(1000, auto_buy_seeds)
        except Exception:
            pass


def main():
    try:
        play_music()
    except Exception:
        pass

    setup_and_gui()

    try:
        root.after(1000, tick)
    except Exception:
        pass

    try:
        plantspersec_job_id = root.after(0, plantspersecond)
    except Exception:
        pass

    try:
        sellpersec_job_id = root.after(0, sellpersecond)
    except Exception:
        pass
    try:
        seed_auto_job_id = root.after(0, auto_buy_seeds)
    except Exception:
        pass

    game_loop()
    root.mainloop()


if __name__ == "__main__":
    main()
