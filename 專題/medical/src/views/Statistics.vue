<template>
  <div class="dashboard">
    <el-card class="card">
      <el-header>
        <div class="filters">
          <div class="filter-item" >
            <h>Week: </h>
            <el-date-picker v-model="selectedWeek" type="date" placeholder="Week" />
          </div>
          <div class="filter-item">
            <h>Month: </h>
            <el-date-picker v-model="selectedMonth" type="month" placeholder="Month" />
          </div>
          <div class="filter-item">
            <h>Year: </h>
            <el-date-picker v-model="selectedYear" type="year" placeholder="Year" />
          </div>

          <!-- 搜尋按鈕 -->
          <el-button type="primary" @click="search" >
            <el-icon><Search /></el-icon>
            Search
          </el-button>

          <!-- 重置按鈕 -->
          <el-button type="danger" @click="resetFilters">
            Reset
          </el-button>
        </div>
      </el-header>

      <!-- 通用 Loading 動畫彈窗 -->
      <el-dialog v-model="loadingDialogVisible" width="30%" :modal="true" :close-on-click-modal="false" :show-close="false">
        <div class="dialog-content" v-loading="loading" element-loading-text="Generating, please wait...">
        </div>
      </el-dialog>

      <!-- 折線圖，根據 searchPerformed 是否顯示 -->
      <div v-if="searchPerformed" class="bertxt1">
        <h>Patient number trend graph:</h>
        <div id="line-chart-container" ref="lineChartContainer" class="chart-container"></div>
      </div>

      <!-- 長條圖，根據 searchPerformed 是否顯示 -->
      <div v-if="searchPerformed" class="bertxt2">
        <h>Patient disease comparison bar chart:</h>
        <div id="bar-chart-container" ref="barChartContainer" class="chart-container"></div>
      </div>

      <!-- More From Statistics 按鈕 -->
      <el-button v-if="searchPerformedbtn" type="primary" class="More" @click="viewMoreStatistics">More From Statistics</el-button>

      <!-- Patients Statistics Analysis，根據 searchPerformed 是否顯示 -->
      <div v-if="GAIData" class="bertxt">
        <h>Patients Statistics Analysis:</h>
        <div id="Statistics-container" class="statistics-container" v-html="GAIData"></div>
      </div>
    </el-card>
  </div>
</template>

<script>
  import * as api from '../api/api.js';
  import axios from 'axios';
  import * as echarts from 'echarts';
  import { ref } from 'vue';

  export default {
    name: 'Statistics',
    data() {
      return {
        loadingDialogVisible: false, // 控制彈窗顯示與否
        loading: false, // 控制 loading 動畫
        selectedWeek: '',
        selectedMonth: '',
        selectedYear: '',
        searchPerformed: false,
        searchPerformedbtn: false,
        Data: null,
        SummaryData: null,
        GAIData: null,
      };
    },
    methods: {
      // 整理日期
      formatDate(date, format) {
        if (!date) return '';
        const options = { year: 'numeric' };
        if (format === 'yyyy/MM/dd') {
          options.month = '2-digit';
          options.day = '2-digit';
        } else if (format === 'yyyy/MM') {
          options.month = '2-digit';
        }
        return new Date(date).toLocaleDateString('zh-TW', options).replace(/\//g, '/');
      },
      // 日期欄位搜尋
      search() {
        this.searchPerformed = true;
        this.searchPerformedbtn = true;
        let mode = '';
        let timeData = '';

        if (this.selectedWeek) {
          mode = 'week';
          timeData = this.formatDate(this.selectedWeek, 'yyyy/MM/dd');
        } else if (this.selectedMonth) {
          mode = 'month';
          timeData = this.formatDate(this.selectedMonth, 'yyyy/MM');
        } else if (this.selectedYear) {
          mode = 'year';
          timeData = this.formatDate(this.selectedYear, 'yyyy');
        } else {
          console.error('請選擇一個日期範圍');
          return;
        }

        console.log(`Searching with mode: ${mode} and date: ${timeData}`);
        this.fetchStatisticsDate(mode, timeData);
        this.fetchStatistics(mode, timeData).then((data) => {
          if (data) {
            this.Data = data;
            this.processData(data);
            //console.log('讓我看看:', data);
            //this.fetchStatisticsDate(data);
          }
        });
        
      },
      // 清空搜尋欄位
      resetFilters() {
        // 清空選擇的日期
        this.selectedWeek = '';
        this.selectedMonth = '';
        this.selectedYear = '';
        // 隱藏圖表和 More From Statistics 按鈕
        this.searchPerformed = false;
        this.searchPerformedbtn = false;
        // 清除圖表內容
        if (this.lineChartInstance) this.lineChartInstance.clear();
        if (this.barChartInstance) this.barChartInstance.clear();
      },
      // Statistic 圖表API
      fetchStatistics(mode, timeData) {
        return axios
          .post(api.domain + '/Statistic/Statistic', { Mode: mode, Date: timeData })
          .then((response) => {
            if (response.data && response.data.Data) {
              return response.data.Data;
            } else {
              console.error('Unexpected response structure:', response);
              return null;
            }
          })
          .catch((error) => {
            console.error('Error fetching appointment details:', error);
            return null;
          });
      },
      // 取得圖表資訊後前端呈現
      processData(data) {
        console.log('Raw data from API:', data);

        // 將原始的折線圖資料提取並轉換為日期物件
        let lineChartData = data.LineChart.Data.map(item => ({
          date: new Date(item.Date),
          count: item.Count
        }));
        lineChartData.sort((a, b) => a.date - b.date);

        // 將原始的條形圖資料轉換為日期物件並排序
        let barChartData = data.BarChart.Data.map(item => ({
          date: new Date(item.Date),
          maleCount: item.MaleCount,
          femaleCount: item.FemaleCount
        }));
        barChartData.sort((a, b) => a.date - b.date);

        // 判斷選取的模式
        const isWeekMode = this.selectedWeek !== '';
        const isMonthMode = this.selectedMonth !== '';
        const isYearMode = this.selectedYear !== '';

        // 如果是月模式，填充當月缺少的日期
        if (isMonthMode) {
          // 將 Date 物件轉換為 "YYYY-MM" 格式的字串
          const year = this.selectedMonth.getFullYear();
          const month = String(this.selectedMonth.getMonth() + 1).padStart(2, '0'); // 月份從 0 開始

          // 檢查轉換後的結果
          console.log(`Parsed selectedMonth as: ${year}-${month}`);

          // 生成當月的所有日期
          const daysInMonth = new Date(year, this.selectedMonth.getMonth() + 1, 0).getDate(); // 獲取該月份的天數
          const allDatesInMonth = Array.from({ length: daysInMonth }, (_, i) => {
            const day = String(i + 1).padStart(2, '0');
            return `${year}-${month}-${day}`;
          });

          // 填補折線圖的缺失日期
          lineChartData = allDatesInMonth.map(date => {
            const existingData = lineChartData.find(item => item.date.toISOString().slice(0, 10) === date);
            return existingData ? existingData : { date: new Date(date), count: 0 };
          });

          // 填補條形圖的缺失日期
          barChartData = allDatesInMonth.map(date => {
            const existingData = barChartData.find(item => item.date.toISOString().slice(0, 10) === date);
            return existingData ? existingData : { date: new Date(date), maleCount: 0, femaleCount: 0 };
          });
        }

        // 根據模式設定 x 軸的日期格式
        const lineChartDates = lineChartData.map(item => item.date.toISOString().slice(0, 10));
        const lineChartCounts = lineChartData.map(item => item.count);

        const barChartDates = barChartData.map(item => {
          if (isWeekMode || isMonthMode) {
            return item.date.toISOString().slice(0, 10); // YYYY-MM-DD
          } else if (isYearMode) {
            return item.date.toISOString().slice(0, 7); // YYYY-MM
          }
          return item.date.toISOString().slice(0, 10);
        });

        // 使用填充後的 barChartData 來生成 maleCounts 和 femaleCounts
        const maleCounts = barChartData.map(item => item.maleCount);
        const femaleCounts = barChartData.map(item => item.femaleCount);

        console.log('Line chart data:', { dates: lineChartDates, counts: lineChartCounts });
        console.log('Bar chart data:', { dates: barChartDates, maleCounts, femaleCounts });

        this.initLineChart({ dates: lineChartDates, counts: lineChartCounts });
        this.initBarChart({ dates: barChartDates, maleCounts, femaleCounts });
      },
      // 折線圖
      initLineChart(data) {
        if (this.$refs.lineChartContainer) {
          this.lineChartInstance = echarts.init(this.$refs.lineChartContainer);
          this.lineChartInstance.setOption({
            tooltip: {
              trigger: 'axis', // 顯示提示訊息
            },
            xAxis: {
              type: 'category',
              data: data.dates,
            },
            yAxis: { type: 'value' },
            series: [{
              data: data.counts,
              type: 'line',
              smooth: false,
            }],
          });
        }
      },
      // 男女條狀圖
      initBarChart(data) {
        if (this.$refs.barChartContainer) {
          this.barChartInstance = echarts.init(this.$refs.barChartContainer);
          this.barChartInstance.setOption({
            tooltip: {
              trigger: 'axis', // 顯示提示訊息
            },
            xAxis: {
              type: 'category',
              data: data.dates,
            },
            yAxis: { type: 'value' },
            series: [
              {
                name: '男生',
                data: data.maleCounts,
                type: 'bar',
                barWidth: '30%',
                itemStyle: { color: '#42A5F5' },
              },
              {
                name: '女生',
                data: data.femaleCounts,
                type: 'bar',
                barWidth: '30%',
                itemStyle: { color: '#f87979' },
              },
            ],
          });
        }
      },
      // 取得 StartDate、EndDate 進行 Summary API
      fetchStatisticsDate(mode, timeData) {
        let StartDate = '';
        let EndDate = '';

        if (mode === 'week') {
          StartDate = timeData;
          const endOfWeek = new Date(timeData);
          endOfWeek.setDate(endOfWeek.getDate() + 6); // 設置一週後的日期
          EndDate = this.formatDate(endOfWeek, 'yyyy/MM/dd');

        } else if (mode === 'month') {
          // 將 timeData 作為日期來初始化，例如 '2024/10'
          const startOfMonth = new Date(timeData + '/01');
          StartDate = this.formatDate(startOfMonth, 'yyyy/MM/dd'); // 設置當月第一天

          const endOfMonth = new Date(startOfMonth);
          endOfMonth.setMonth(startOfMonth.getMonth() + 1); // 移動到下個月
          endOfMonth.setDate(0); // 設置為當月的最後一天
          EndDate = this.formatDate(endOfMonth, 'yyyy/MM/dd');

        } else if (mode === 'year') {
          const year = parseInt(timeData, 10); // 將 timeData 轉換為年份數字
          const startOfYear = new Date(year, 0, 1); // 設置為當年第一天
          StartDate = this.formatDate(startOfYear, 'yyyy/MM/dd');
          const endOfYear = new Date(year, 11, 31); // 設置為當年最後一天
          EndDate = this.formatDate(endOfYear, 'yyyy/MM/dd');

        } else {
          console.error('請選擇一個日期範圍');
          return;
        }

        console.log(`Searching with mode: ${mode}, StartDate: ${StartDate}, EndDate: ${EndDate}`);

        axios
          .post(api.domain + '/Statistic/Summary', { StartDate, EndDate })
          .then((response) => {
            if (response.data && response.data.Data) {
              this.SummaryData = response.data.Data;
              console.log('搶先看:',this.SummaryData);
            } else {
              console.error('Unexpected response structure:', response);
            }
          })
          .catch((error) => {
            console.error('Error fetching appointment details:', error);
          });
      },
      // 病症統計
      viewMoreStatistics() {
        // 顯示 loading 視窗
        this.loadingDialogVisible = true;
        this.loading = true;

        // 使用 this.$nextTick 確保視窗已顯示後再進行 API 請求
        this.$nextTick(() => {
          const rawData = this.SummaryData;

          // 1. 按日期分組並轉換為 string
          const groupedByDate = rawData.reduce((acc, record) => {
            const date = record.AppointmentDate;
            if (!acc[date]) acc[date] = [];
            acc[date].push(record.FinalDiagnosis);
            return acc;
          }, {});

          const groupedByDateString = Object.entries(groupedByDate)
            .map(([date, diagnoses]) => `${date}: ${diagnoses.join(', ')}`)
            .join('\n');

          // 2. 性別統計數據並轉換為 string
          const genderStatistics = rawData.reduce((acc, record) => {
            const sex = record.Sex;
            acc[sex] = (acc[sex] || 0) + 1;
            return acc;
          }, { M: 0, F: 0 });

          const genderStatisticsString = `Male: ${genderStatistics.M}, Female: ${genderStatistics.F}`;

          // 3. 診斷次數並轉換為 string
          const diagnosisCount = rawData.reduce((acc, record) => {
            const diagnosis = record.FinalDiagnosis;
            acc[diagnosis] = (acc[diagnosis] || 0) + 1;
            return acc;
          }, {});

          const diagnosisCountString = Object.entries(diagnosisCount)
            .map(([diagnosis, count]) => `${diagnosis}: ${count}`)
            .join('\n');

          // 4. 合併成單一字串
          const analysisDataString = `
            Grouped By Date:
            ${groupedByDateString}

            Gender Statistics:
            ${genderStatisticsString}

            Diagnosis Count:
            ${diagnosisCountString}
          `;

          // 將合併後的字串存入 analysisData，供 API 使用
          this.analysisData = analysisDataString.trim();
          
          // 發送 API 請求
          axios
            .post('http://127.0.0.1:8000/Statistics', { diagnosisInfo: this.analysisData })
            .then((response) => {
              if (response.data) {
                // 提取 content 屬性中的字串資料
                this.GAIData = response.data.content;
                this.GAIData = this.GAIData
                  .replace(/###\s*/g, '')           // 移除 ### 標記及其後的空白
                  .replace(/\*\*(.*?)\*\*/g, '$1')  // 移除 **粗體** 標記
                  .replace(/\*(.*?)\*/g, '$1')      // 移除 *斜體* 標記
                  .replace(/^\s+|\s+$/g, '')        // 去除首尾的多餘空白
                this.searchPerformedbtn = false;
                console.log(this.GAIData);
              } else {
                console.error('Unexpected response structure:', response);
              }
            })
            .catch((error) => {
              console.error('Error fetching patient details:', error);
            })
            .finally(() => {
              // 無論請求成功或失敗，關閉 loading 視窗
              this.loadingDialogVisible = false;
              this.loading = false;
            });
        });
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
    align-items: center;
    gap: 10px;
    background-color: #E1F5F2;
    box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
    border-radius: 20px;
    padding: 10px 15px;
    width: 100%;
    height: 80px;
    flex-wrap: wrap; /* 允許項目換行 */
  }

  .el-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .bertxt{
    margin-top: 40px;
    margin-left: 20px;
  }
  .bertxt1 {
    margin-top: 40px;
    margin-left: 20px;
  }
  .bertxt2 {
    margin-top: 40px;
    margin-left: 20px;
  }

  .chart-container {
    width: 100%;
    height: 400px;
    background-color: #f9fafc;
    box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
    border-radius: 20px;
    margin-top: 20px;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .el-button {
    border-radius: 16px;
  }
  .statistics-container {
    width: 97%;
    background-color: #f9fafc;
    box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
    border-radius: 20px;
    margin-top: 20px;
    padding: 20px;
    line-height: 1.6; /* Increase line height for better readability */
    font-size: 16px;  /* Adjust font size if necessary */
    white-space: pre-wrap; /* Respect line breaks and spacing */
  }

  .card {
    background-color: #eaf5fc;
    border-radius: 20px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    padding: 20px;
    min-height: 250px;
  }
  
  .More {
    background: linear-gradient(135deg, #B9C3F5, #DD73DF);
    color: #fff;
    border-radius: 16px;
    margin-top: 20px;
    margin-left: 50%;
    transform: translateX(-50%);
  }
}
@media (max-width: 800px){
  .dialog-content {
    display: flex;
    justify-content: center;
    align-items: center;
    height: auto;
    font-size: 16px;
  }
  .filters {
    margin-top: 90px;
    display: flex;
    align-items: center;
    background-color: #E1F5F2;
    box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
    width: 100%;
    height: auto;
    flex-wrap: wrap; /* 允許項目換行 */
  }

  .el-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .bertxt1 {
    margin-top: 130px;
  }
  .bertxt2 {
    margin-top: 30px;
  }

  .chart-container {
    width: 100%;
    height: 400px;
    background-color: #f9fafc;
    box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
    border-radius: 20px;
    margin-top: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .el-button {
    margin-left: 35px;
    border-radius: 16px;
  }
  .statistics-container {
    width: 100%;
    background-color: #f9fafc;
    box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
    border-radius: 20px;
    margin-top: 20px;
    padding: 20px;
    line-height: 1.6; /* Increase line height for better readability */
    font-size: 16px;  /* Adjust font size if necessary */
    white-space: pre-wrap; /* Respect line breaks and spacing */
  }

  .card {
    background-color: #eaf5fc;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  }
  
  .More {
    background: linear-gradient(135deg, #B9C3F5, #DD73DF);
    color: #fff;
    border-radius: 16px;
    margin-top: 20px;
    margin-left: 50%;
    transform: translateX(-50%);
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
    align-items: center;
    gap: 30px;
    background-color: #E1F5F2;
    box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
    border-radius: 20px;
    padding-left: 20px;
    width: 100%;
    height: 80px;
  }

  .el-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .bertxt1 {
    margin-top: 40px;
    margin-left: 20px;
  }
  .bertxt2 {
    margin-top: 40px;
    margin-left: 20px;
  }

  .chart-container {
    width: 100%;
    height: 400px;
    background-color: #f9fafc;
    box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
    border-radius: 20px;
    margin-top: 20px;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .statistics-container {
    width: 97%;
    background-color: #f9fafc;
    box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
    border-radius: 20px;
    margin-top: 20px;
    padding: 20px;
    line-height: 1.6; /* Increase line height for better readability */
    font-size: 16px;  /* Adjust font size if necessary */
    white-space: pre-wrap; /* Respect line breaks and spacing */
  }

  .el-button {
    border-radius: 16px;
    margin-right: 15px;

  }

  .card {
    background-color: #eaf5fc;
    border-radius: 20px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    padding: 20px;
  }

  .More {
    background: linear-gradient(135deg, #B9C3F5, #DD73DF);
    color: #fff;
    border-radius: 16px;
    margin-top: 20px;
    margin-left: 50%;
    transform: translateX(-50%);
  }
}
</style>