from django.http import HttpResponse
from django.shortcuts import render
from Crypto.Cipher import AES
from django.utils.encoding import smart_text

from Crypto import Random
from transliterate import translit
from Crypto.Random import random
import  string
import uuid

from .forms import Secure_Text_Class


def split_every(n, s):
    return [s[i:i + n] for i in range(0, len(s), n)]


def main_page(request):
    if request.method == 'GET':
        return render(request, 'main_page/main.html')
    elif request.method == 'POST':
        form = Secure_Text_Class(request.POST)
        if form.is_valid():
            # I am saving just the id of encrypted text that would be saved in db
            # so the key would be known just by user.

            the_SECURE_DATA = form.cleaned_data['secured_text'] # not in DB
            print(the_SECURE_DATA)
            for_aes = 16 - len(the_SECURE_DATA)
            randy = Random.new()

            IV = randy.read(16)  # IV saved in DB

            the_key_to_ENCRYPT = randy.read(random.choice([16, 24, 32]))

            the_key_to_FIND = uuid.uuid4().hex  # saved in DB

            aes_crypt = AES.new(the_key_to_ENCRYPT, AES.MODE_CBC, IV)

            splited_array = []

            if for_aes >= 0:

                the_SECURE_DATA = the_SECURE_DATA.ljust(16, '~')

                encrypted_text = aes_crypt.encrypt(the_SECURE_DATA)

            else:

                splited_array.append(split_every(16, the_SECURE_DATA))

                redefined_array = []

                for per_ellement in splited_array[0]:

                    if len(per_ellement) < 16:

                        updated_part = str(per_ellement).ljust(16, '~')

                        redefined_array.append(updated_part)

                    else:

                        redefined_array.append(per_ellement)
                arr = []
                for ready in redefined_array:


                    encrypted_text = aes_crypt.encrypt(ready)
                    print(
                        'text: ' + str(encrypted_text), '\n'
                                                        'key: ' + str(the_key_to_ENCRYPT), '\n'
                                                                                           'iv:' + str(IV)
                    )
                    decrypt = AES.new(the_key_to_ENCRYPT, AES.MODE_CBC, IV)


                    arr.append(str(decrypt.decrypt(encrypted_text),'utf-8'))

                print(', '.join([str(x) for x in arr]))
            exit(the_SECURE_DATA)
            return HttpResponse(str(encrypted_text))

        else:

            return HttpResponse('Not valid')

    return render(request, 'main_page/main.html')
