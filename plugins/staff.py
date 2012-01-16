class plugin(object):

    commands = {
        "staff": "staff"
    }

    def __init__(self, irc):
        self.irc = irc

    def getStaff(self):
        users = urllib.urlopen('http://www.mcbans.com/staff?getStaff').read()
        return users.split("\n")

    def getUser(users, user):
        for rawline in users:
            splitline = rawline.split(':')
            if splitline[0] == user or splitline[1] == user:
                return splitline
        return 'NOUSER'

    def getUserInfo(user, rank):
        return urllib.urlopen('http://www.mcbans.com/staff?getInfoOn=' + user + '&staffRank=' + rank).read()

    def stripHtml(input):
        input = string.replace(input, '<br/>', "\n")
        p = re.compile(r'<[^<]*?/?>')
        q = re.compile(r'\n{2,}')
        output = q.sub("\n", p.sub('', input))
        output = string.replace(output, '\nPosition Title:', ' - Position Title:')
        output = string.replace(output, 'About Me:\n', 'About Me: ')
        return output

    def staff(self, user, channel, arguments):
        "Get information about our staff members"
        self.irc.sendnotice(user, "Success!")
        if len(arguments) < 2:
            self.irc.sendnotice(user, 'You must provide a username.')
        users = self.getStaff()
        user = self.getUser(users, arguments[1])
        if user == 'NOUSER':
            self.irc.sendnotice(user, 'No staff member by this name exists.')
        self.irc.sendnotice(user, self.stripHtml(self.getUserInfo(user[0], user[2])))

    hooks = {}

    name = "Staff Information"