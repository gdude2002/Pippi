import random
from system.yaml_loader import *

class plugin(object):
    """
    Play russian roulette, the safe way!
    """

    commands = {
        "put"       : "put",
        "give"      : "put",
        "get"       : "get",
        "remove"    : "remove",
        "inventory" : "inventory"
    }

    hooks = {
        "connectionLost": "save",
        "signedOn": "load",
        }

    def __init__(self, irc):
        self.irc = irc
        self.items_handler = yaml_loader(True, "items")
        self.items = self.items_handler.load("items")
        if not self.items:
            self.items = {}

        self.channels = {}
        self.users = {}

        self.help = {
            "put": "Add an item to the bot's inventory.\nUsage: %sput <item>" % self.irc.control_char,
            "give": "Add an item to the bot's inventory (Alias of put).\nUsage: %sgive <item>" % self.irc.control_char,
            "get": "Get a random item from the bot's inventory.\nUsage: %sget" % self.irc.control_char,
            "remove": "Remove an item from the bot's inventory.\nUsage: %sremove <item>\nNOTE: Needs op or higher" % self.irc.control_char
            ,
            "inventory": "Get a list of items in the bot's inventory.\nUsage: %sinventory <item>\nNOTE: Needs op or higher" % self.irc.control_char
            ,
            }

    def load(self, data=None):
        self.items = self.items_handler.load("items")

        if not self.items:
            self.items = {}

    def save(self, data=None):
        self.items_handler.save_data("items", self.items)

    def put(self, user, channel, arguments):
        if len(arguments) > 1:
            item = " ".join(arguments[1:]).lower()
            if item not in self.items.keys():
                self.items[item] = {"name": item, "owner": user}
                self.irc.send_raw(
                    "PRIVMSG " + channel + " :\1ACTION takes " + user + "'s " + item + " and puts it in her bag.\1")
                self.save()
            else:
                self.irc.send_raw(
                    "PRIVMSG " + channel + " :\1ACTION already has someone's " + item + " in her bag!\1")
        else:
            self.irc.sendnotice(user, "Usage: %sput <item>" % self.irc.control_char)

    def get(self, user, channel, arguments):
        if self.items.keys():
            random.seed()
            items = self.items.keys()
            itemn = items[random.randint(0, len(items) - 1)]
            item = self.items[itemn]
            self.irc.send_raw(
                "PRIVMSG " + channel + " :\1ACTION takes " + item["owner"] + "'s " + item["name"] +
                " out of her bag and gives it to " + user + ".\1")

            del self.items[itemn]

            self.save()
        else:
            self.irc.send_raw(
                "PRIVMSG " + channel + " :\1ACTION has no items in her bag!\1")

    def remove(self, user, channel, arguments):
        if self.irc.is_op(channel, user) or user in self.authorized.keys():
            if len(arguments) > 1:
                item = " ".join(arguments[1:]).lower()
                if item in self.items.keys():
                    del self.items[item]
                    self.save()
                    self.irc.sendnotice(user, "Item %s removed." % item)
                else:
                    self.irc.sendnotice(user, "Item %s does not exist." % item)
            else:
                self.irc.sendnotice(user, "Usage: %sremove <item>" % self.irc.control_char)
        else:
            self.irc.sendnotice(user, "You do not have access to this command.")

    def inventory(self, user, channel, arguments):
        if self.irc.is_op(channel, user) or user in self.authorized.keys():
            if self.items.keys():
                items = self.items
                itemlist = sorted(self.items.keys())

                while itemlist:
                    done = []
                    for i in range(0, 5):
                        if itemlist:
                            item = itemlist.pop(0)
                            stuff = items[item]["name"] + "|" + items[item]["owner"]
                            done.append(stuff)
                        else:
                            break
                    self.irc.sendnotice(user, ", ".join(done))
                    del done
            else:
                self.irc.sendnotice(user, "There are no items in the inventory.")
        else:
            self.irc.sendnotice(user, "You do not have access to this command.")

    name = "Items"
