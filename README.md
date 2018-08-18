# cninfo_retriever
This is a bunch of python 2/3 tools for retrieving PDF files from http://www.cninfo.com.cn/cninfo-new/index

## Usage:
1. The pdfRetrieve.bat will run pdfRetrieve3.py, which will create directory Report20XX and start downloading files to this directory
2. Please move getData.bat, getData2.py, pdfToTxt.bat and pdfToTxt2.py to the directory Report20XX
3. Download pdfminer and install it (You can download it from https://pypi.org/project/pdfminer/ or you can try 
``` pip install pdfminer```
)
4. Run pdfToTxt.bat
5. Run getData.bat. It will attemp to get data from PFDs and store them into result.csv
6. Now open result.csv with Microsoft Excel. Decode it in Unicode(UTF-8).
