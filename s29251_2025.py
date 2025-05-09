# generator_fasta.py

# CEL PROGRAMU:
# Program służy do generowania losowej sekwencji DNA zapisanej w formacie FASTA.
# Użytkownik podaje długość sekwencji, identyfikator (ID), opis oraz swoje imię, które zostaje wstawione w losowe miejsce w sekwencji.
# Program zapisuje wynik do pliku oraz oblicza statystyki zawartości nukleotydów A, C, G, T i procent zawartości CG względem AT.

# KONTEKST ZASTOSOWANIA:
# Program ten może być wykorzystywany w edukacji biologii molekularnej, bioinformatyce oraz testowaniu narzędzi analizujących dane FASTA.

import random  # biblioteka do losowego generowania sekwencji
from collections import Counter  # do zliczania wystąpień nukleotydów

# Pobieranie danych od użytkownika
length = int(input("Podaj długość sekwencji: "))  # użytkownik podaje długość sekwencji, która jest konwertowana na liczbę całkowitą
seq_id = input("Podaj ID sekwencji: ")  # użytkownik podaje identyfikator sekwencji
description = input("Podaj opis sekwencji: ")  # użytkownik podaje opis sekwencji
name = input("Podaj imię: ")  # użytkownik podaje imię, które zostanie wstawione w sekwencję

# Lista nukleotydów DNA
nucleotides = ['A', 'C', 'G', 'T']  # lista zawierająca cztery podstawowe zasady azotowe w DNA

# GENEROWANIE LOSOWEJ SEKWENCJI DNA

# ORIGINAL:
# sequence = ''.join(random.choices(nucleotides, k=length))
# MODIFIED (dodano obsługę błędów i walidację długości):
if length <= 0:
    raise ValueError("Długość sekwencji musi być większa od zera.")  # zabezpieczenie przed nieprawidłową długością sekwencji
sequence = ''.join(random.choices(nucleotides, k=length))  # generowanie losowej sekwencji o zadanej długości

# WSTAWIENIE IMIENIA W LOSOWE MIEJSCE

# ORIGINAL:
# insert_pos = random.randint(0, len(sequence))
# sequence_with_name = sequence[:insert_pos] + name + sequence[insert_pos:]
# MODIFIED (lepsza czytelność, jawna zmienna):
insertion_position = random.randint(0, len(sequence))  # losowe wybranie pozycji, w której zostanie wstawione imię
sequence_with_name = sequence[:insertion_position] + name + sequence[insertion_position:]  # wstawienie imienia do sekwencji

# ZAPIS DO PLIKU FASTA

# ORIGINAL:
# with open(f"{seq_id}.fasta", "w") as fasta_file:
#     fasta_file.write(f">{seq_id} {description}\n")
#     fasta_file.write(sequence_with_name)
# MODIFIED (dodano łamanie sekwencji co 60 znaków - lepsza zgodność z formatem FASTA):
with open(f"{seq_id}.fasta", "w") as fasta_file:  # otwarcie pliku do zapisu, nazwa pliku zgodna z ID
    fasta_file.write(f">{seq_id} {description}\n")  # zapis nagłówka FASTA (identyfikator i opis)
    for i in range(0, len(sequence_with_name), 60):  # podział sekwencji na linie co 60 znaków (zgodnie ze standardem FASTA)
        fasta_file.write(sequence_with_name[i:i+60] + "\n")  # zapis fragmentów sekwencji do pliku z nową linią

print(f"Sekwencja została zapisana do pliku {seq_id}.fasta")  # informacja dla użytkownika o zapisaniu pliku

# STATYSTYKI SEKWENCJI (BEZ IMIENIA)

# ORIGINAL:
# counts = Counter(sequence)
# MODIFIED (dodano dzielenie przez długość i formatowanie wyników):
counts = Counter(sequence)  # zliczenie wystąpień każdego nukleotydu w oryginalnej sekwencji (bez imienia)
total = len(sequence)  # obliczenie całkowitej długości oryginalnej sekwencji

# Obliczanie procentowej zawartości nukleotydów
percentages = {nuc: (counts[nuc] / total) * 100 for nuc in nucleotides}  # obliczenie procentowego udziału każdego nukleotydu

# Wyświetlanie wyników
print("Statystyki sekwencji:")
for nuc in nucleotides:
    print(f"{nuc}: {percentages[nuc]:.1f}%")  # wyświetlenie procentowej zawartości każdego nukleotydu (zaokrąglone do 1 miejsca po przecinku)

# Obliczanie stosunku CG do AT
cg = counts['C'] + counts['G']  # suma wystąpień cytozyny i guaniny
at = counts['A'] + counts['T']  # suma wystąpień adeniny i tyminy
cg_ratio = (cg / (cg + at)) * 100 if (cg + at) != 0 else 0  # obliczenie procentowego udziału CG względem AT, z zabezpieczeniem przed dzieleniem przez zero
print(f"%CG: {cg_ratio:.1f}")  # wyświetlenie wyniku zawartości CG

# DODATKOWE ULEPSZENIA:
# MODIFIED (dodano walidację ID i opisu - pozwala tylko litery, cyfry i spacje w opisie):
# Zapewnia to kompatybilność z wymaganiami formatów bioinformatycznych.

import re  # import modułu do obsługi wyrażeń regularnych
if not re.match(r"^[\w-]+$", seq_id):  # sprawdzenie czy ID zawiera tylko litery, cyfry i myślnik
    raise ValueError("ID sekwencji może zawierać tylko litery, cyfry i znak '-'.")  # komunikat błędu przy nieprawidłowym ID

if not re.match(r"^[\w\s.,'-]*$", description):  # sprawdzenie czy opis zawiera tylko dozwolone znaki
    raise ValueError("Opis sekwencji może zawierać tylko litery, cyfry, spacje oraz znaki . , ' -")  # komunikat błędu przy nieprawidłowym opisie

# KONIEC PROGRAMU
