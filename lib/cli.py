#!/usr/bin/env python

from sqlalchemy import create_engine
from models import Base, Trainer, Pokemon
from sqlalchemy.orm import sessionmaker
import ipdb
import os
from random import randint


class Cli():
    def start(self):
        self.clear()
        print("Welcome to the wonderful world of pokemon!")
        self.wait()
        print("let's get started!")
        self.wait()
        self.login_or_create()

    def login_or_create(self):
        print("Type 1 to Create Account")
        print("Type 2 to Login")
        print("Type 3 to exit")
        user_input = self.choice()
        self.process_login_or_create(user_input)

    def process_login_or_create(self, user_input):
        if user_input == "1":
            self.create()
        elif user_input == "2":
            self.login()
        elif user_input == "3":
            self.goodbye()
        else:
            self.invalid()
            self.wait()
            self.clear()
            self.login_or_create()

    def login(self):
        self.clear()
        print("What is your name?")
        name = self.choice()
        existing_trainer = Trainer.find_by_name(session, name)
        if existing_trainer:
            self.trainer = existing_trainer
            self.welcome_trainer()
        else:
            print("Trainer does not exist")
            self.wait()
            self.login_or_create()

    def create(self):
        self.clear()
        print("What is your name?")
        name = self.choice()
        existing_trainer = Trainer.find_by_name(session, name)
        if existing_trainer:
            self.clear()
            print("Trainer name already taken")
            self.wait()
            self.login_or_create()
        else:
            self.trainer = Trainer(name=name)
            session.add(self.trainer)
            session.commit()
            self.welcome_trainer()

    def welcome_trainer(self):
        self.clear()
        print(f"Welcome {self.trainer.name}!")
        print("Your journey is about to begin.")
        self.wait()
        self.menu()

    def menu(self):
        self.clear()
        print("Here is your selection: ")
        print("Type 1 to create a pokemon")
        print("Type 2 to discover a new pokemon to catch!")
        print("Type 3 to list your caught pokemon")
        print("Type 4 to exit")
        self.menu_choice()

    def menu_choice(self):
        user_input = self.choice()
        self.clear()
        options = {
            "1": self.create_pokemon,
            "2": self.discover_pokemon,
            "3": self.list_pokemons,
            "4": self.goodbye
        }

        fnc = options.get(user_input, self.invalid)
        fnc()

    def catch_menu(self, pokemon):
        if pokemon in self.trainer.pokemons:
            print("You already own this pokemon")
        else:
            print("Would you like to catch this pokemon? (Y/N)")
            user_input = self.choice()
            self.clear()
            if user_input.lower() == "y":
                self.trainer.catch_pokemon(session, pokemon)
                print(f"You caught { pokemon.name }")
            else:
                print(f"{pokemon.name} ran away...")
        self.wait()
        self.menu()

    def create_pokemon(self):
        print("What is the pokemon's name?")
        name = self.choice()
        self.clear()
        print("What is the pokemons national dex id?")
        pokedex_id = self.choice()
        self.clear()

        existing_pokemon = Pokemon.find_by_name(session, name)
        self.clear()
        if existing_pokemon:
            print("Pokemon already exist, please create another one")
        else:
            pokemon = Pokemon(name=name, pokedex_id=pokedex_id)
            session.add(pokemon)
            session.commit()
            self.clear()
            print(f"{pokemon.name} was created.")
        self.wait()
        self.menu()

    def discover_pokemon(self):
        pokemons = Pokemon.all(session)
        idx = randint(0, len(pokemons) - 1)
        pokemon = pokemons[idx]
        self.clear()
        print(f"A wild {pokemon.name} appeared!")
        self.wait()
        self.catch_menu(pokemon)

    def list_pokemons(self):
        ordered_trainer_pokemons = self.trainer.sorted_pokemons()
        print("-----------------")
        print("Printing Pokemons")
        print("-----------------")
        print("")
        print_lines = [
            f"Pokedex # { pokemon.pokedex_id } | { pokemon.name }" for pokemon in ordered_trainer_pokemons]
        for line in print_lines:
            print(line)
            print("-----------------")
        self.wait()
        self.menu()

    def choice(self):
        return input("Enter Here: ")

    def clear(self):
        os.system("clear")

    def wait(self):
        input("")

    def invalid(self):
        print("Invalid Choice")

    def goodbye(self):
        print("Leaving the world of pokemon and shutting down...")


if __name__ == "__main__":
    engine = create_engine("sqlite:///pokemon.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    Cli().start()
