
class KoreanTokenRefiner:

    def __init__(self):
        self.particles = [
            '은','는','이','가',
            '을','를',
            '이','그','저',
            '에','에서','으로','으로부터','로부터',
        ]

    def refine(self, tokens):
        new_tokens = []
        for par in self.particles:
            p = re.compile(f"{par}$")
            for token in tokens:
                if p.search(string=token) is None:
                    new_tokens.append(token)
                else:
                    new_tokens.append(p.sub(string=token, repl=''))
        new_tokens = list(set(new_tokens))
        return new_tokens
