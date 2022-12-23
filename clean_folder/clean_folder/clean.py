from pathlib import *
import shutil
import sys, re, rarfile, zipfile, lzma, py7zr
import rarfile
import os
from unicodedata import normalize, is_normalized


# Списки розширень для сортування
list_img = ['.JPEG', '.jpeg', '.PNG', '.png', '.JPG', '.jpg', '.SVG', '.svg']
list_archive = ['.rar', '.RAR', '.zip', '.ZIP',
                '.gz', '.GZ', '.tar', '.TAR', '.7z', '.7Z']
list_video = ['.AVI', '.avi', '.MP4', '.mp4', '.MOV', '.mov', '.MKV', '.mkv']
list_documents = ['.DOC', '.doc', '.DOCX', '.docs', '.TXT', '.txt',
                  '.PDF', '.pdf', '.XLSX', '.xlsx', '.PPTX', '.pptx', '.xml', '.XML']
list_music = ['.MP3', '.mp3', '.OGG', '.ogg', '.WAV', '.wav', '.AMR', '.amr']

# Загальний список файлів
rez = []


# Списки відсортованих файлів
rez_img = []
rez_archive = []
rez_video = []
rez_documents = []
rez_music = []
rez_other = []

# Список знайдених розширень
suffix_img = set()
suffix_archive = set()
suffix_video = set()
suffix_document = set()
suffix_music = set()
suffix_other = set()

#Нормалізуємо назву файлу
def normalize_file(name_file):
    new_name_file = normalize('NFC', name_file)
    shutil.move(name_file, new_name_file)

# Аналіз папки з файлами та ігнорування папок якщо в назві міститься "sorted"+ нормалізація
def analiz_files(path_file):
    for i in os.listdir(path_file):
        if is_normalized('NFC', i) == False:
            print('Нормалізуємо назву файлу ', i)
            normalize(i)
        adres_string = str(Path(path_file + '\\' + i))      
        
        if re.search('sorted', adres_string) == None:
            if os.path.isdir(path_file + '\\' + i):
                
                analiz_files(path_file + '\\' + i)
            else:
                rez.append(adres_string)
                
                
    return rez      
    


# Створюємо папку для відсортованих файлів
def create_folder(path_folder, name_folder):
    new_folder = Path(path_folder) / name_folder
    if not Path.exists(new_folder):
        Path.mkdir(new_folder)
        
        

# Складаємо список знайдених суфіксів
def create_list_suffix():
    for j in rez:        
        if Path(j).suffix in list_img:
            rez_img.append(j)
            suffix_img.add(Path(j).suffix)
        elif Path(j).suffix in list_archive:
            rez_archive.append(j)
            suffix_archive.add(Path(j).suffix)
        elif Path(j).suffix in list_video:
            rez_video.append(j)
            suffix_video.add(Path(j).suffix)
        elif Path(j).suffix in list_music:
            rez_music.append(j)
            suffix_music.add(Path(j).suffix)
        elif Path(j).suffix in list_documents:
            rez_documents.append(j)
            suffix_document.add(Path(j).suffix)
        else:
            rez_other.append(j)
            suffix_other.add(Path(j).suffix)


#Переносимо файли у відповідні папки
def move_files(rez_file, folder_move):
    for file_rez in rez_file:        
        shutil.move(Path(sys.argv[1], file_rez ), folder_move)

#Розпаковуємо архіви, якщо вони є, та видаляємо самі архіви після розпакування
def unpack_archive():
    try:
        folder_archive = sys.argv[1] + '\\archive_sorted'
        for archive in os.listdir(folder_archive):
            if Path(archive).suffix == '.zip' or Path(archive).suffix == '.tar' or Path(archive).suffix == '.gz':
                 file_for_unpack = zipfile.ZipFile(folder_archive +'\\'+archive)
                 file_for_unpack.extractall(folder_archive)
                 file_for_unpack.close()
                 root_for_delete = Path(folder_archive + '\\'+archive)
                 try:
                    Path.unlink(root_for_delete)
                 except OSError as e:
                    print("Error: %s : %s" % (root_for_delete, e.strerror))                
            
            elif Path(archive).suffix == '.7z':
                path_archive = folder_archive+'\\'+ archive 
                file_for_unpack = py7zr.SevenZipFile(path_archive, mode='r')
                file_for_unpack.extractall(folder_archive + '\\' + Path(archive).stem)
                file_for_unpack.close()
                root_for_delete = Path(folder_archive + '\\'+archive)
                try:
                    Path.unlink(root_for_delete)
                except OSError as e:
                    print("Error: %s : %s" % (root_for_delete, e.strerror))   
    except:
        print('Архівів для розпакування не знайдено')       
        

    

# Виводимо повідомлення про знайдене та створюємо папки
def report_create_folder():
    if len(suffix_img) > 0:
        print('__________________________________________________________')
        print('__________________________________________________________')
        print('Результат фото (знайдені розширення та відповідні файли):')
        print('Розширення фото:')
        for d in suffix_img:
            print(d)
        print('__________________________________________________________')
        print('Файли фото:')
        count_foto = 0
        for g in rez_img:
            list_split_name = g.split('\\')
            print(list_split_name[-1])
            #print(g)
            count_foto = count_foto + 1            
        create_folder(sys.argv[1], 'image_sorted')
        
        move_files(rez_img, Path(sys.argv[1], 'image_sorted'))
        
    else:
        print('__________________________________________________________')
        print('Несортованих файлів типу "Зображення" не знайдено.')
        print('__________________________________________________________')
        
    if len(suffix_archive) > 0:
        print('__________________________________________________________')
        print('__________________________________________________________')
        print('Результат архіви (знайдені розширення та відповідні файли):')
        print('Розширення архівів:')
        for h in suffix_archive:
            print(h)
        print('__________________________________________________________')
        print('Файли архівів:')
        count_archive = 0
        for k in rez_archive:
            list_split_name = k.split('\\')
            print(list_split_name[-1])
            #print(k)
            count_archive = count_archive + 1
        create_folder(sys.argv[1], 'archive_sorted')
        move_files(rez_archive, Path(sys.argv[1], 'archive_sorted'))        
        unpack_archive() 
        
        
    else:
        print('__________________________________________________________')
        print('Несортованих файлів типу "Архів" не знайдено.')
        print('__________________________________________________________')
    
    
        
    if len(suffix_video) > 0:
        print('__________________________________________________________')
        print('__________________________________________________________')
        print('Результат відео (знайдені розширення та відповідні файли):')
        print('__________________________________________________________')
        print('Розширення відео:')
        for l in suffix_video:
            print(l)
        print('__________________________________________________________')
        print('Файли відео:')
        count_video = 0
        for z in rez_video:
            list_split_name = z.split('\\')
            print(list_split_name[-1])
            #print(z)
            count_video = count_video + 1
        create_folder(sys.argv[1], 'video_sorted')
        move_files(rez_video, Path(sys.argv[1], 'video_sorted'))
    else:
        print('__________________________________________________________')
        print('Несортованих файлів типу "Відео" не знайдено.')
        print('__________________________________________________________')

    if len(suffix_music) > 0:
        print('__________________________________________________________')
        print('__________________________________________________________')
        print('Результат музика (знайдені розширення та відповідні файли):')
        print('__________________________________________________________')
        print('Розширення музика:')
        for x in suffix_music:
            print(x)
        print('__________________________________________________________')
        print('Файли музика:')
        count_music = 0
        for c in rez_music:
            list_split_name = c.split('\\')
            print(list_split_name[-1])
            #print(c)
            count_music = count_music + 1
        create_folder(sys.argv[1], 'music_sorted')
        move_files(rez_music, Path(sys.argv[1], 'music_sorted'))
    else:
        print('__________________________________________________________')
        print('Несортованих файлів типу "Музика" не знайдено.')
        print('__________________________________________________________')

    if len(suffix_document) > 0:
        print('__________________________________________________________')
        print('Результат документи (знайдені розширення та відповідні файли):')
        print('__________________________________________________________')
        print('Розширення документи')
        for v in suffix_document:           
            print(v)
        print('__________________________________________________________')
        print('Файли документів:')
        count_documents = 0
        for b in rez_documents:
            list_split_name = b.split('\\')
            print(list_split_name[-1])
            #print(b)
            count_documents = count_documents + 1
        create_folder(sys.argv[1], 'documents_sorted')
        move_files(rez_documents, Path(sys.argv[1], 'documents_sorted'))
    else:
        print('__________________________________________________________')
        print('Несортованих файлів типу "Текстовий документ" не знайдено.')
        print('__________________________________________________________')
        
    if len(suffix_other) > 0:
        print('__________________________________________________________')
        print('Результат інші файли (знайдені розширення та відповідні файли):')
        print('__________________________________________________________')
        print('Розширення інше:')
        for n in suffix_other:
            print(n)
        print('__________________________________________________________')
        print('Файли інше:')
        count_other = 0
        for m in rez_other:
            list_split_name = m.split('\\')
            print(list_split_name[-1])
            #print(m)
            count_other = count_other + 1
        create_folder(sys.argv[1], 'other_sorted')
        move_files(rez_other, Path(sys.argv[1], 'other_sorted'))
    else:
        print('__________________________________________________________')
        print('Несортованих файлів невідомого типу не знайдено.')
        print('__________________________________________________________')


#Видаляємо пусті папки з-під файлів
def delete_empty_folder(path_for_delete):
    
    try:        
        for i in os.listdir(path_for_delete):
            adres_path = Path(path_for_delete + '\\' + i)
            if re.search('sorted', str(adres_path)) == None:                
                try:
                    shutil.rmtree(adres_path)
                except OSError as e:
                    print("Error: %s : %s" % (str(adres_path), e.strerror))                    
    except:
        print('Папок для видалення не знайдено')     



# Головна процедура для проведення розбору файлів
def __main__():
    try:
        dyrectory_current = sys.argv[1]
        analiz_files(dyrectory_current)
        create_list_suffix()
        report_create_folder()   
        unpack_archive() 
        delete_empty_folder(dyrectory_current)  

    except:
        print('Введіть шлях до папки')


__main__()
