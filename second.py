import time
from bs4 import BeautifulSoup
import requests
from links import all_links
from first import open_and_save
import csv
import os
import urllib
import urllib3
from urllib.request import urlopen
from PIL import Image, UnidentifiedImageError
from short_about import all_about as all_descr


def save_csv(data):
    with open('data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)


def save_photo(link, name, bar_id, r):
    p = requests.get(link)
    out = open(f"img/{bar_id}/{name}{r}", "wb")
    out.write(p.content)
    time.sleep(1)
    out.close()

    try:
        im = Image.open(f"img/{bar_id}/{name}{r}")
    except Exception:
        time.sleep(2)
        p = requests.get(link)
        out = open(f"img/{bar_id}/{name}{r}", "wb")
        out.write(p.content)
        out.close()

    try:
        im = Image.open(f"img/{bar_id}/{name}{r}")
    except Exception as err:
        time.sleep(2)
        p = urllib.request.urlopen(link)
        out = open(f"img/{bar_id}/{name}{r}", "wb")
        out.write(p.read())
        out.close()

        try:
            im = Image.open(f"img/{bar_id}/{name}{r}")
        except Exception as err:
            time.sleep(2)
            p = urllib3.request('get', link)
            out = open(f"img/{bar_id}/{name}{r}", "wb")
            out.write(p.read())
            out.close()

            try:
                im = Image.open(f"img/{bar_id}/{name}{r}")
            except Exception as err:
                with open('err.csv', 'a') as file:
                    writer = csv.writer(file)
                    writer.writerow([bar_id, link])
                os.remove(f"img/{bar_id}/{name}{r}")


def get_info():
    bar_id = 1
    for i in all_links:
        link = f"https://www.restoclub.ru{i}"
        key_name = i.replace("/spb/place/", "")
        res = open_and_save(link, key_name)
        soup = BeautifulSoup(res, "lxml")

        try:
            name = soup.find(class_="place-title__header").text
            print(name)
            addr = soup.find(class_="place__aside").find(class_="t-dotted").text.replace(" ", ' ')
            print(addr)
            phone = soup.find(class_="place-phone__number").get("content")
            print(phone)
            if not phone:
                phone = soup.find(class_="place-phone__popup").find(class_="modal _slide _dropdown _round phone-list-popup").find(class_="phone-list__link").get("href")
                if phone:
                    phone = str(phone).replace("tel:", "")
                    print(phone)
            rating = soup.find(class_="place__rating").find(class_="place-rating__value").find(class_="rating__value").text
            print(rating)
            full_text = soup.find(class_="expandable-text__t").text.replace("Текст предоставлен заведением", "").strip()
            print(full_text)
            time_work = soup.find("div", class_="place__info").find(class_="info__list-item")
            if time_work:
                time_work = time_work.text
            else:
                time_work = '-'
            print(time_work)
            key_name = i.replace("/spb/place/", "")
            print(key_name)
            data = [bar_id, name, addr, phone, rating, full_text, time_work, key_name, all_descr[bar_id - 1]]
            save_csv(data)

        except Exception as ex_:
            # with open('errLink.csv', 'a') as file:
            #     writer = csv.writer(file)
            #     writer.writerow([link])
            print(f"[ERR] Something went wrong\n{ex_}")
            time.sleep(1)
            print(f"-------------->{link}")
            data = [link]
            save_csv(data)
            continue


        try:
            os.mkdir(f"img/{key_name}")
            name = 2
            photo = soup.find(class_="gallery-photo").find('img').get("src")
            try:
                if str(photo)[:1] == "/":
                    l2 = f"https://www.restoclub.ru{photo}"
                    save_photo(l2, name, key_name, ".jpg")
                else:
                    save_photo(photo, name, key_name, ".webp")

            except Exception as ex_:
                print(ex_)
            name += 1

            photo2 = soup.find_all(class_="gallery-photo _cover")
            for j in photo2:
                if j.get("data-src"):
                    try:
                        if str(j.get("data-src"))[:1] == "/":
                            l2 = f"https://www.restoclub.ru{j.get('data-src')}"
                            save_photo(l2, name, key_name, ".jpg")
                            time.sleep(1)
                        else:
                            save_photo(j.get("data-src"), name, key_name, ".webp")
                        name += 1
                    except:
                        continue


        except Exception as _ex:
            print(_ex)

        finally:
            bar_id += 1
            print(f"[INFO] {bar_id}: Success")

    print(f"[SUCCESS] Finished")


if __name__ == "__main__":
    get_info()
