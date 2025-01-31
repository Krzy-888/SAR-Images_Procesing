import streamlit as st
import rasterio
import numpy as np
from scipy.signal import convolve2d
import os
import cv2
import io
#funkcje
def dBsc(obraz):
    return np.log10(obraz)*10


def srednia(obraz,ksize):
    k_half = ksize//2
    usredniony_obraz = np.ones((obraz.shape[0],obraz.shape[1]))
    obraz_2 = np.zeros((obraz.shape[0]+k_half*2,obraz.shape[1]+k_half*2))
    obraz_2[k_half:obraz.shape[0]+k_half,k_half:obraz.shape[1]+k_half] = obraz
    for i in range(k_half,obraz.shape[0]+k_half):
        for j in range(k_half,obraz.shape[1]+k_half):
            usredniony_obraz[i-k_half,j-k_half] = obraz_2[i-k_half:i+k_half+1,j-k_half:j+k_half+1].mean()
    return usredniony_obraz

def wariancja(obraz,ksize):
    k_half = ksize//2
    variance_img = np.ones((obraz.shape[0],obraz.shape[1]))
    obraz_2 = np.zeros((obraz.shape[0]+k_half*2,obraz.shape[1]+k_half*2))
    obraz_2[k_half:obraz.shape[0]+k_half,k_half:obraz.shape[1]+k_half] = obraz
    for i in range(k_half,obraz.shape[0]+k_half):
        for j in range(k_half,obraz.shape[1]+k_half):
            variance_img[i-k_half,j-k_half] = obraz_2[i-k_half:i+k_half+1,j-k_half:j+k_half+1].var()
    return variance_img

def kowariancja(srednia,wariancja):
    return wariancja/srednia
#filtr Lee
def Lee(obraz,ksize):
    kernel_1 = np.ones((ksize,ksize))/(ksize**2)
    res = convolve2d(obraz, kernel_1, 'same','symm')
    return res
#Filtr Gamma MAP
def gammaMap(obraz,ksize):
    kernel_1 = np.ones((ksize,ksize))/(ksize**2)
    res = convolve2d(obraz, kernel_1, 'same','symm')
    return res

plik = st.file_uploader("daj obraz")
if plik is not None:
    with rasterio.open(io.BytesIO(plik.getvalue())) as SAR:
        #SAR = rasterio.open(calosc)
        sar_img = SAR.read(1)
        sar_img_n = cv2.convertScaleAbs(sar_img)
        #sar_img_n = normalizuj_obraz(sar_img)

    st.image(sar_img_n)
    option = st.selectbox('Wybierz metodę przetwarzania:',('Uśredniający','Pow2dB','Gamma Map', 'Frost', 'Lee'))
    if option=='Uśredniający':
        ksize = st.selectbox('Wybierz rozmiar maski:',(3,5,7, 9, 11))
        kernel_1 = np.ones((ksize,ksize))/(ksize**2)
        res = convolve2d(sar_img, kernel_1, 'same','symm')
        sar_img_n2 = cv2.convertScaleAbs(res)
        st.image(sar_img_n2)
        st.balloons()
    elif option=='Pow2dB':
        sar_img_dB = dBsc(sar_img)
        sar_img_n2 = cv2.convertScaleAbs(sar_img_dB)
        st.image(sar_img_n2)
        st.balloons()
    elif option=='Gamma Map':
        ksize = st.selectbox('Wybierz rozmiar maski:',(3,5,7, 9, 11))
        kernel_1 = np.ones((ksize,ksize))/(ksize**2)
        res = convolve2d(sar_img, kernel_1, 'same','symm')
        sar_img_n2 = cv2.convertScaleAbs(res)
        st.image(sar_img_n2)
        st.balloons()
    elif option=='Frost':
        ksize = st.selectbox('Wybierz rozmiar maski:',(3,5,7, 9, 11))
        kernel_1 = np.ones((ksize,ksize))/(ksize**2)
        res = convolve2d(sar_img, kernel_1, 'same','symm')
        sar_img_n2 = cv2.convertScaleAbs(res)
        st.image(sar_img_n2)
        st.balloons()
    elif option=='Lee':
        ksize = st.selectbox('Wybierz rozmiar maski:',(3,5,7, 9, 11))
        kernel_1 = np.ones((ksize,ksize))/(ksize**2)
        res = convolve2d(sar_img, kernel_1, 'same','symm')
        sar_img_n2 = cv2.convertScaleAbs(res)
        st.image(sar_img_n2)
        st.balloons()




