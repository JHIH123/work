<template>
  <div class="dashboard">
    <el-card class="card">
      <el-header>
        <div class="filters">
          <div class="Search">
            <label for="site-search">Patient ID: </label>
            <input type="search" v-model="patientID" id="site-search" name="q" class="search-input" />
            <el-date-picker
              v-model="selectedDate"
              type="daterange"
              range-separator="To"
              start-placeholder="Start Date"
              end-placeholder="End Date"
              unlink-panels
              :shortcuts="shortcuts"
            />

            <el-button class="search-button" type="primary" @click="search">
              <el-icon><Search /></el-icon>
              Search
            </el-button>
          </div>
        </div>
      </el-header>

      <!-- 通用 Loading 動畫彈窗 -->
      <el-dialog v-model="loadingDialogVisible" width="30%" :modal="true" :close-on-click-modal="false" :show-close="false">
        <div class="dialog-content" v-loading="loading" element-loading-text="Generating, please wait...">
        </div>
      </el-dialog>


      <div class="card2">
        <ul v-if="patientAnalysis">
          <strong>Analyze results:</strong>
          <div class="custom-text" v-if="patientAnalysis" v-html="patientAnalysis"></div>
        </ul>
        
        <el-button v-if="patientAnalysis" class="Referral-button" type="success" @click="showReferralDialog = true">
            <img src="@/assets/Referral.png" alt="Referral" class="Referral-icon" /> Referral
        </el-button>
      </div>

      <el-dialog
        title="Referral"
        v-model="showReferralDialog"
        width="65%"
        @close="closeReferralDialog">
        
        <el-form :model="referralData" label-width="140px" class="custom-form">
          <el-row>
            <el-col :span="11">
              <el-form-item label="Name:">
                <el-input v-model="referralData.name"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="11" :offset="1">
              <el-form-item label="Birthday:">
                <el-date-picker v-model="referralData.birthday" type="date"></el-date-picker>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row>
            <el-col :span="11">
              <el-form-item label="ID card:">
                <el-input v-model="referralData.idCard"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="11" :offset="1">
              <el-form-item label="NHI card:">
                <el-input v-model="referralData.nhiCard"></el-input>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row>
            <el-col :span="11">
              <el-form-item label="Phone No:">
                <el-input v-model="referralData.phoneNo"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="11" :offset="1">
              <el-form-item label="Sex:">
                <el-select v-model="referralData.sex" maxlength="1">
                  <el-option label="M" value="M" />
                  <el-option label="F" value="F" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row>
            <el-col :span="22" :offset="1">
              <el-form-item label="Address:" label-width="70px">
                <el-input v-model="referralData.address" type="textarea"></el-input>
              </el-form-item>
            </el-col>
          </el-row>

          <hr class="divider" />

          <el-row>
            <el-col :span="11">
              <el-form-item label="Clinic Name:">
                <el-input v-model="referralData.clinicName"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="11" :offset="1">
              <el-form-item label="Doctor Name:">
                <el-input v-model="referralData.doctorName"></el-input>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row>
            <el-col :span="11">
              <el-form-item label="Clinic Phone:">
                <el-input v-model="referralData.clinicPhone"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="11" :offset="1">
              <el-form-item label="Order Time:">
                <el-date-picker v-model="referralData.orderTime" type="datetime"></el-date-picker>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row>
            <el-col :span="22" :offset="1">
              <el-form-item label="Recommended Referral Clinic or Suggested Referral Clinic:" label-width="260px">
                <el-input v-model="referralData.recommendedReferralClinic" type="textarea"></el-input>
              </el-form-item>
            </el-col>
          </el-row>

          <hr class="divider" />

          <el-row>
            <el-col :span="22" :offset="1">
              <el-form-item label="Chief Complaint:" label-width="140px">
                <el-input v-model="referralData.chiefComplaint" type="textarea"></el-input>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row>
            <el-col :span="22" :offset="1">
              <el-form-item label="Diagnosis:" label-width="140px">
                <el-input v-model="referralData.diagnosis" type="textarea"></el-input>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row>
            <el-col :span="22" :offset="1">
              <el-form-item label="Reason for Referral:" label-width="140px">
                <el-input v-model="referralData.reasonForReferral" type="textarea"></el-input>
              </el-form-item>
            </el-col>
          </el-row>

        </el-form>

        <!-- 底部的下載按鈕 -->
        <span slot="footer" class="dialog-footer">
          <el-button class="ReferralDownload" @click="DownloadReferral">
            <el-icon> <Download /> </el-icon> download
          </el-button>
        </span>
      </el-dialog>

    </el-card>
  </div>
</template>

<script>
import * as api from '../api/api.js';
import axios from 'axios';
import { PDFDocument, rgb } from 'pdf-lib';
import * as fontkit from 'fontkit';
import Swal from 'sweetalert2';
import { ref } from 'vue';

function drawMultilineTextByCharacters(page, text, x, y, font, fontSize, color, maxCharsPerLine, lineHeight) {
  let currentY = y;
  let currentLine = '';

  for (let i = 0; i < text.length; i++) {
    currentLine += text[i];

    // 當達到最大字數或遇到換行符時，繪製文字並移動到下一行
    if (currentLine.length >= maxCharsPerLine || text[i] === '\n') {
      page.drawText(currentLine.trim(), { x, y: currentY, size: fontSize, font, color });
      currentY -= lineHeight;
      currentLine = '';
    }
  }

  // 繪製剩餘文字
  if (currentLine.length > 0) {
    page.drawText(currentLine.trim(), { x, y: currentY, size: fontSize, font, color });
  }
}

async function DownloadReferral() {
  // 切割 `birthday` 成 `birthYear`、`birthMonth`、`birthDay`
  if (this.referralData.birthday) {
    const birthDate = new Date(this.referralData.birthday);
    this.referralData.birthYear = birthDate.getFullYear().toString();
    this.referralData.birthMonth = (birthDate.getMonth() + 1).toString().padStart(2, '0');
    this.referralData.birthDay = birthDate.getDate().toString().padStart(2, '0');
  }

  // 切割 `orderTime` 成 `orderYear`、`orderMonth`、`orderDay`
  if (this.referralData.orderTime) {
    const orderDate = new Date(this.referralData.orderTime);
    this.referralData.orderYear = orderDate.getFullYear().toString();
    this.referralData.orderMonth = (orderDate.getMonth() + 1).toString().padStart(2, '0');
    this.referralData.orderDay = orderDate.getDate().toString().padStart(2, '0');
  }

  // 根據 `sex` 設定 `sexMaleChecked` 和 `sexFemaleChecked`
  if (this.referralData.sex) {
    this.referralData.sexMaleChecked = this.referralData.sex === 'M';
    this.referralData.sexFemaleChecked = this.referralData.sex === 'F';
  }

  try {
    // 1. 加載背景圖片
    const imageUrl = '/Referral Form.png'; 
    const response = await fetch(imageUrl);
    const imageBytes = await response.arrayBuffer();

    // 2. 建立 PDF 文檔並嵌入自定義字型
    const pdfDoc = await PDFDocument.create();
    pdfDoc.registerFontkit(fontkit);

    const fontUrl = new URL('@/assets/NotoSansTC-VariableFont_wght.ttf', import.meta.url).href;
    const fontBytes = await fetch(fontUrl).then(res => res.arrayBuffer());
    const customFont = await pdfDoc.embedFont(fontBytes);

    const asciiFontUrl = new URL('@/assets/Roboto-Thin.ttf', import.meta.url).href;
    const asciiFontBytes = await fetch(asciiFontUrl).then((res) => res.arrayBuffer());
    const asciiFont = await pdfDoc.embedFont(asciiFontBytes);

    const page = pdfDoc.addPage([595, 842]); // A4 大小

    // 3. 嵌入圖片到 PDF 作為背景
    const pngImage = await pdfDoc.embedPng(imageBytes);
    page.drawImage(pngImage, {
      x: 0,
      y: 0,
      width: page.getWidth(),
      height: page.getHeight(),
    });

    // 4. 設置文字樣式和顏色
    const fontSize = 12;
    const textColor = rgb(0, 0, 0);

    // 姓名
    page.drawText(`${this.referralData.name}`, { x: 90, y: 752, size: fontSize, color: textColor, font: customFont });

    // 性別
    const maleCheck = this.referralData.sexMaleChecked ? '✓' : '';
    const femaleCheck = this.referralData.sexFemaleChecked ? '✓' : '';
    page.drawText(`${maleCheck}`, { x: 190, y: 757, size: fontSize, color: textColor, font: customFont });
    page.drawText(`${femaleCheck}`, { x: 224, y: 757, size: fontSize, color: textColor, font: customFont });

    // 出生日期
    page.drawText(`${this.referralData.birthYear}`, {
      x: 300, y: 752, size: fontSize, color: textColor, font: customFont,
    });
    page.drawText(`${this.referralData.birthMonth}`, {
      x: 356, y: 752, size: fontSize, color: textColor, font: customFont,
    });
    page.drawText(`${this.referralData.birthDay}`, {
      x: 399, y: 752, size: fontSize, color: textColor, font: customFont,
    });

    // 健保卡
    page.drawText(`${this.referralData.nhiCard}`, { x: 452, y: 752, size: fontSize, color: textColor, font: customFont });
    // 身分證
    page.drawText(`${this.referralData.idCard}`, { x: 90, y: 693, size: fontSize, color: textColor, font: asciiFont });
    // 病患連絡電話
    page.drawText(`${this.referralData.phoneNo}`, { x: 178, y: 693, size: fontSize, color: textColor, font: customFont });
    // 病患地址
    page.drawText(`${this.referralData.address}`, { x: 300, y: 693, size: fontSize, color: textColor, font: customFont });

    // 主訴
    drawMultilineTextByCharacters(page, this.referralData.chiefComplaint, 108, 659, customFont, fontSize, textColor, 38, 16);
    // 診斷
    drawMultilineTextByCharacters(page, this.referralData.diagnosis, 108, 499, customFont, fontSize, textColor, 38, 16);
    // 轉診目的
    drawMultilineTextByCharacters(page, this.referralData.reasonForReferral, 86, 386, customFont, fontSize, textColor, 38, 16);
    
    // 診所名稱
    page.drawText(`${this.referralData.clinicName}`, { x: 60, y: 293, size: fontSize, color: textColor, font: customFont });
    // 醫生名字
    page.drawText(`${this.referralData.doctorName}`, { x: 176, y: 293, size: fontSize, color: textColor, font: customFont });
    // 診所電話
    page.drawText(`${this.referralData.clinicPhone}`, { x: 295, y: 293, size: fontSize, color: textColor, font: customFont });
    // 預約時間
    page.drawText(`${this.referralData.orderYear}`, {
      x: 405, y: 293, size: fontSize, color: textColor, font: customFont,
    });
    page.drawText(`${this.referralData.orderMonth}`, {
      x: 460, y: 293, size: fontSize, color: textColor, font: customFont,
    });
    page.drawText(`${this.referralData.orderDay}`, {
      x: 508, y: 293, size: fontSize, color: textColor, font: customFont,
    });

    // 建議轉診的診所名稱
    page.drawText(`${this.referralData.recommendedReferralClinic}`, { x: 176, y: 273, size: fontSize, color: textColor, font: customFont });

    // 6. 生成 PDF 並下載
    const pdfBytes = await pdfDoc.save();
    const blob = new Blob([pdfBytes], { type: 'application/pdf' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'Referral.pdf';
    link.click();
  } catch (error) {
    console.error('生成 PDF 時出現錯誤:', error);
  }
}


export default {
  setup() {
    const selectedDate = ref(''); // 只在 setup 中定義 selectedDate
    const shortcuts = [
      {
        text: '近一週',
        value: () => {
          const end = new Date();
          const start = new Date();
          start.setDate(start.getDate() - 7);
          return [start, end];
        },
      },
      {
        text: '近一個月',
        value: () => {
          const end = new Date();
          const start = new Date();
          start.setMonth(start.getMonth() - 1);
          return [start, end];
        },
      },
      {
        text: '近半年',
        value: () => {
          const end = new Date();
          const start = new Date();
          start.setMonth(start.getMonth() - 6);
          return [start, end];
        },
      },
      {
        text: '近一年',
        value: () => {
          const end = new Date();
          const start = new Date();
          start.setFullYear(start.getFullYear() - 1);
          return [start, end];
        },
      },
    ];

    const search = () => {
      console.log('Selected date range:', selectedDate.value);
    };

    return {
      selectedDate,
      shortcuts,
      search,
    };
  },
  data() {
    return {
      loadingDialogVisible: false, // 控制彈窗顯示與否
      loading: false, // 控制 loading 動畫
      showReferralDialog: false, // Referral 視窗
      capturedImageData: null, // 用來儲存捕捉到的圖片數據
      referralData: {
        name: '',                       // 病人姓名
        birthday: '',
        birthYear: '',                  // 生日年份
        birthMonth: '',                 // 生日月份
        birthDay: '',                   // 生日日期
        idCard: '',                     // 身分證字號
        nhiCard: '',                    // 健保卡號
        phoneNo: '',                    // 聯絡電話
        sex: '',
        sexMaleChecked: false,          // 男性勾選
        sexFemaleChecked: false,        // 女性勾選
        address: '',                    // 地址
        clinicName: '',                 // 診所名稱
        doctorName: '',                 // 醫生名稱
        clinicPhone: '',                // 診所電話
        orderTime: '',
        orderYear: '',                  // 預約年份
        orderMonth: '',                 // 預約月份
        orderDay: '',                   // 預約日期
        recommendedReferralClinic: '',  // 推薦轉診診所
        chiefComplaint: '',             // 主訴
        diagnosis: '',                  // 診斷
        reasonForReferral: ''           // 轉診原因
      },
      patientID: '', // 儲存使用者輸入的 Patient ID
      finalDiagnosisList: [], // 儲存彙整的診斷資訊，包括 AppointmentDate, ChiefComplaint 和 FinalDiagnosis
      diagnosisString: '', // 儲存格式化後的診斷資訊字串
      patientAnalysis: '', // 要分析用的資料      
    };
  },
  methods: {
    DownloadReferral,
    async search() {
      //console.log('查看目前的時間選取範圍:', this.selectedDate);
      try {
        if (this.patientID && this.selectedDate && this.selectedDate.length === 2) {
          const formatDate = (date) => {
            const year = date.getFullYear();
            const month = (date.getMonth() + 1).toString().padStart(2, '0');
            const day = date.getDate().toString().padStart(2, '0');
            return `${year}-${month}-${day}`;
          };

          const startDate = new Date(this.selectedDate[0]);
          const endDate = new Date(this.selectedDate[1]);

          // 生成日期範圍
          const dateList = [];
          for (let d = startDate; d <= endDate; d.setDate(d.getDate() + 1)) {
            dateList.push(formatDate(new Date(d))); // 克隆日期，避免引用錯誤
          }

          // 依次查詢每個日期，並合併結果
          const allAppointments = [];
          for (const date of dateList) {
            //console.log('確認現在時間:',date);
            const response = await axios.post(api.domain + '/Appointment/AppointmentList', { 
              PatientID: this.patientID,
              Date: date
            });

            if (response.data && response.data.Data) {
              allAppointments.push(...response.data.Data);
              //console.log('查看預約列表陣列:',allAppointments);
            }
          }

          if (allAppointments.length > 0) {
            // 收集每個 AppointmentID 的診斷資料
            const diagnosisPromises = allAppointments.map(appointment =>
              axios.post(api.domain + '/Diagnosis/DiagnosisInfo', { AppointmentID: appointment.AppointmentID })
            );

            // 執行所有的 Diagnosis 查詢請求
            const diagnosisResponses = await Promise.all(diagnosisPromises);

            // 彙整資料
            this.finalDiagnosisList = diagnosisResponses.map((response, index) => ({
              AppointmentID: allAppointments[index].AppointmentID,
              AppointmentDate: allAppointments[index].AppointmentDate,
              ChiefComplaint: response.data.Data ? response.data.Data.ChiefComplaint : 'N/A',
              FinalDiagnosis: response.data.Data ? response.data.Data.FinalDiagnosis : 'N/A'
            }));

            this.formatDiagnosisString();
          } else {
            Swal.fire({
              icon: "info",
              title: "No Records Found",
              text: "No appointments found within the selected date range.",
            });
          }
        } else {
          Swal.fire({
            icon: "error",
            title: "Something went wrong!",
            text: "Please check your patient ID and selected Dates.",
          });
        }
      } catch (error) {
        console.error('Error fetching appointment or diagnosis details:', error);
      }
    },

    
    // 格式化診斷資料成字串格式
    formatDiagnosisString() {
      // 格式化每筆診斷資料
      const formattedDetails = this.finalDiagnosisList
        .map(diagnosis => 
          `Appointment Date: ${diagnosis.AppointmentDate}, Chief Complaint: ${diagnosis.ChiefComplaint}, Final Diagnosis: ${diagnosis.FinalDiagnosis}`
        )
        .join(' | \n'); // 使用 ' | ' 和換行符號分隔每筆資料

      // 合併開頭和每筆診斷資料
      this.diagnosisString = `${formattedDetails}`;
      
      console.log(this.diagnosisString);
      this.GetpatientAnalysis();
    },
    
    // 使用診斷資料字串的 API 請求方法
    async GetpatientAnalysis() {
      // 顯示彈窗和 loading
      this.loadingDialogVisible = true;
      this.loading = true;

      try {
        const response = await axios.post('http://127.0.0.1:8000/PatientAnalysis', { diagnosisInfo: this.diagnosisString });
        
        if (response.data) {
          // 對取得的分析結果進行格式化處理
          this.patientAnalysis = response.data.content
            .replace(/\*\*(.*?)\*\*/g, '$1')  // 移除 **粗體** 標記
            .replace(/###\s*/g, '')           // 移除 ### 標記及其後面的空白
            .replace(/\*(.*?)\*/g, '$1')     // 移除 *斜體* 標記
            .replace(/\n/g, '<br>');           // 將換行符號替換為 <br>

          console.log(this.patientAnalysis);
        } else {
          console.error('Unexpected response structure:', response);
        }
      } catch (error) {
        console.error('Error fetching patient details:', error);
      } finally {
        this.loadingDialogVisible = false; // 關閉彈窗
        this.loading = false; // 停止 loading
      }
    },
    
    
      
  },
};
</script>

<style scoped>

@media (max-width: 1024px){
  .dialog-content {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100px;
    font-size: 16px;
  }
  .filters {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    gap: 20px;
  }
  .el-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .A {
    border-radius: 20px;
    background-color: #c1f8e56b;
    padding: 6px;
    width: 550px;
  }
  .el-button {
    border-radius: 20px;
  }
  .card {
    margin-left: 10px;
    background-color: #eaf5fc;
    border-radius: 20px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    padding: 10px;
  }
  .date {
    margin-left: 10px;
  }
  .Search {
    padding: 13px;
    background-color: #dcddffc4;
    border-radius: 15px;
    margin-top: -20px;
  }
  .search-button {
    margin-left: 10px;
  }
  .card2 {
    margin-left: 17px;
    background-color: #ffffff;
    padding: 20px;
    border-radius: 20px;
    margin-top: 5px;
    position: relative; /* 確保子元素可以絕對定位於 card2 */
  }
  .Referral-icon{
    width: 26%;
  }
  .Referral-button{
    position: absolute;
    bottom: 10px; /* 距離 card2 底部的距離 */
    right: 20px;  /* 距離 card2 右側的距離 */
    display: flex;
    align-items: center;
    width: auto; /* 自適應按鈕內容的寬度 */
    min-width: unset; /* 移除默認最小寬度 */
    max-width: 100px; /* 可選，限制按鈕最大寬度 */
    white-space: nowrap; /* 避免按鈕內文字換行 */
    overflow: hidden; /* 隱藏可能的超出部分 */
    background-color: #69CC9A;
  }
  .Referral-button:hover{
    background-color: #539e79;
  }
  .dialog-footer {
    margin-left: 90%;
  }
  .ReferralDownload {
    margin-left: -70px;
    border-radius: 13px;
    background-color: #B098E2;
    color: #ffffff;
  }
  .ReferralDownload.active {
    background-color: #947ec4;
    color: #dddddd;
  }
  .ReferralDownload:hover {
    background-color: #947ec4;
    color: #dddddd;
  }
  .search-input {
    width: 200px;
    height: 28px;
    border-radius: 4px;
    border: 1px solid #b3b3b3;
    font-size: 14px;
    color: #000000;
    margin-right: 10px;
  }
}

@media (min-width: 800px){
  .dialog-content {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100px;
    font-size: 16px;
  }
  .filters {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    gap: 20px;
  }
  .el-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .A {
    border-radius: 20px;
    background-color: #c1f8e56b;
    padding: 6px;
    width: 550px;
  }
  .el-button {
    border-radius: 20px;
  }
  .card {
    margin-left: -10px;
    background-color: #eaf5fc;
    border-radius: 20px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    padding: 10px;
  }
  .date {
    margin-left: 10px;
  }
  .Search {
    padding: 13px;
    background-color: #dcddffc4;
    border-radius: 15px;
    margin-top: 30px;
  }
  .search-button {
    margin-top: 10px;
    margin-left: 10px;
  }
  .card2 {
    margin-left: 7px;
    background-color: #ffffff;
    padding: 5px 20px 30px 0;
    border-radius: 20px;
    margin-top: 70px;
    position: relative; /* 確保子元素可以絕對定位於 card2 */
  }
  .Referral-icon{
    width: 26%;
  }
  .Referral-button{
    position: absolute;
    bottom: 10px; /* 距離 card2 底部的距離 */
    right: 20px;  /* 距離 card2 右側的距離 */
    display: flex;
    align-items: center;
    width: auto; /* 自適應按鈕內容的寬度 */
    min-width: unset; /* 移除默認最小寬度 */
    max-width: 100px; /* 可選，限制按鈕最大寬度 */
    white-space: nowrap; /* 避免按鈕內文字換行 */
    overflow: hidden; /* 隱藏可能的超出部分 */
    background-color: #69CC9A;
  }
  .Referral-button:hover{
    background-color: #539e79;
  }
  .dialog-footer {
    margin-left: 90%;
  }
  .ReferralDownload {
    margin-left: -70px;
    border-radius: 13px;
    background-color: #B098E2;
    color: #ffffff;
  }
  .ReferralDownload.active {
    background-color: #947ec4;
    color: #dddddd;
  }
  .ReferralDownload:hover {
    background-color: #947ec4;
    color: #dddddd;
  }
  .search-input {
    margin-bottom: 10px;
    width: 200px;
    height: 28px;
    border-radius: 4px;
    border: 1px solid #b3b3b3;
    font-size: 14px;
    color: #000000;
    margin-right: 10px;
  }
}
@media (min-width: 1024px){
  .dialog-content {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100px;
    font-size: 16px;
  }
  .filters {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    gap: 20px;
  }
  .el-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .A {
    border-radius: 20px;
    background-color: #c1f8e56b;
    padding: 6px;
    width: 550px;
  }
  .el-button {
    border-radius: 20px;
  }
  .card {
    margin-left: 10px;
    background-color: #eaf5fc;
    border-radius: 20px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    padding: 10px;
  }
  .date {
    margin-left: 10px;
  }

  .Search {
    padding: 13px;
    background-color: #dcddffc4;
    border-radius: 15px;
    margin-top: -20px;
  }
  .search-button {
    margin-left: 10px;
  }
  .card2 {
    margin-left: 17px;
    background-color: #ffffff;
    padding: 20px;
    border-radius: 20px;
    margin-top: 5px;
    position: relative; /* 確保子元素可以絕對定位於 card2 */
  }
  .Referral-icon{
    width: 26%;
  }
  .Referral-button{
    position: absolute;
    bottom: 10px; /* 距離 card2 底部的距離 */
    right: 20px;  /* 距離 card2 右側的距離 */
    display: flex;
    align-items: center;
    width: auto; /* 自適應按鈕內容的寬度 */
    min-width: unset; /* 移除默認最小寬度 */
    max-width: 100px; /* 可選，限制按鈕最大寬度 */
    white-space: nowrap; /* 避免按鈕內文字換行 */
    overflow: hidden; /* 隱藏可能的超出部分 */
    background-color: #69CC9A;
  }
  .Referral-button:hover{
    background-color: #539e79;
  }
  .dialog-footer {
    margin-left: 90%;
  }
  .ReferralDownload {
    border-radius: 13px;
    background-color: #B098E2;
    color: #ffffff;
  }
  .ReferralDownload.active {
    background-color: #947ec4;
    color: #dddddd;
  }
  .ReferralDownload:hover {
    background-color: #947ec4;
    color: #dddddd;
  }

  .search-input {
    width: 200px;
    height: 28px;
    border-radius: 4px;
    border: 1px solid #b3b3b3;
    font-size: 14px;
    color: #000000;
    margin-right: 10px;
  }

}
  
</style>
