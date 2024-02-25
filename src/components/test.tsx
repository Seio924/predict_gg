import * as fs from 'fs';

function readTxtFromTSX(filePath: string): string[] {
    let dataList: string[] = [];
    try {
        const content: string = fs.readFileSync(filePath, 'utf-8');
        dataList = content.split('\n');
    } catch (error) {
        console.error('Error reading file:', error);
    }
    return dataList;
}

// TSX 파일의 경로를 지정합니다.
const tsxFilePath: string = 'src/predict_data.txt';

// TSX 파일에서 텍스트를 읽어와서 배열로 변환합니다.
const tsxTextList: string[] = readTxtFromTSX(tsxFilePath);

// 변환된 배열을 출력합니다.
console.log(tsxTextList);
