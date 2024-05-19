from src import Client, RSA


if __name__ == '__main__':
    rsa = RSA(seed=0)
    alice = Client(name='Alice', keypair=rsa.generate_keypair())
    bob = Client(name='Bob', keypair=rsa.generate_keypair())
    
    # Sending messages
    alice.send_message(
        user=bob,
        message='Hi Bob! How are you?'
    )
    bob.send_message(
        user=alice,
        message='I am fine, what about you?'
    )
    alice.send_message(
        user=bob,
        message='I am testing my implementation of the RSA algorithm!'
    )
    bob.send_message(
        user=alice,
        message='Cool.'
    )
    