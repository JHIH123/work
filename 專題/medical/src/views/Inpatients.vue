<template>
  <div class="dashboard">
    <el-card class="card">
      <div class="header">
        <el-button type="primary" @click="openSearchDialog">
          <el-icon><Search /></el-icon>
          Search
        </el-button>
        <el-button type="success" @click="handleNewButtonClick">
          <el-icon><Plus /></el-icon>
          New
        </el-button>
      </div>
      <el-tabs v-model="activeTab" @tab-click="handleTabClick">
        <el-tab-pane label="Inpatient" name="Inpatient"> 
          
          <el-table :data="tableData" style="width: 100%" @sort-change="handleSortChange">
            <el-table-column prop="InpatientID" label="InpatientID" width="140" sortable="custom"></el-table-column>
            <el-table-column prop="PatientID" label="Patient ID" width="140" sortable="custom"></el-table-column>
            <el-table-column prop="HospitalDate" label="Hospitalization date" width="200" sortable="custom"></el-table-column>
            <el-table-column prop="DischargedDate" label="Expected Discharge date" width="220" sortable="custom"></el-table-column>
            <el-table-column prop="HospitalBed" label="Hospital Bed" width="150" sortable="custom"></el-table-column>
            <el-table-column prop="AdmissionType" label="Admission type" width="170" sortable="custom"></el-table-column>
            <el-table-column prop="IsPaid" label="IsPaid" width="110" sortable="custom"></el-table-column>
            <el-table-column label="Operations" width="145">
              <template #default="scope">
                <el-icon @click="InpatientsEdit(scope.row)" size="small">
                  <Edit />
                </el-icon>
                <el-icon @click="confirmDelete(scope.$index, scope.row.InpatientID)" size="small">
                  <Delete />
                </el-icon>
              </template>
            </el-table-column>
          </el-table>


          <!-- 搜尋視窗 Inpatients -->
          <el-dialog title="Inpatient" v-model="searchDialogVisible" width="50%">
            <el-form :model="searchForm" label-width="170px">
              <el-form-item label="InpatientID:">
                <el-input v-model="searchForm.InpatientID" placeholder="Please enter a Registration Code"></el-input>
              </el-form-item>
              <el-form-item label="Patient ID:">
                <el-input v-model="searchForm.PatientID" placeholder="Please enter a Patient ID"></el-input>
              </el-form-item>
              <el-form-item label="Hospitalization date:">
                <el-date-picker
                  v-model="searchForm.HospitalDate"
                  type="date"
                  placeholder="Please select a Hospitalization Date"
                  style="width: 100%;">
                </el-date-picker>
              </el-form-item>
              <el-form-item label="Hospital Bed:">
                <el-input v-model="searchForm.HospitalBed" placeholder="Please enter a Hospital Bed"></el-input>
              </el-form-item>
              <el-form-item label="Admission type:">
                <el-input v-model="searchForm.AdmissionType" placeholder="Please enter an Admission Type"></el-input>
              </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
              <el-button @click="resetSearchForm">Reset</el-button>
              <el-button type="primary" @click="searchInpatient">Search</el-button>
            </span>
          </el-dialog>
        </el-tab-pane>

        
      </el-tabs>
    </el-card>
    <!-- 确保 DeleteConfirmation 组件已正确引用 -->
    <DeleteConfirmation ref="deleteConfirmation" />
  </div>
</template>

<script>
import { Edit, Delete, Plus, Search } from '@element-plus/icons-vue';
import DeleteConfirmation from '../components/DeleteConfirmation.vue';
import dayjs from 'dayjs';
import * as api from '../api/api.js';
import axios from 'axios';

export default {
  name: 'Inpatients',
  components: {
    Edit,
    Delete,
    Plus,
    Search,
    DeleteConfirmation,
  },
  data() {
    return {
      activeTab: 'Inpatient', 
      searchDialogVisible: false,
      searchForm: {
        InpatientID: '',
        PatientID: '',
        HospitalDate: '',
        DischargedDate: '',
        HospitalBed: '',
        AdmissionType: '',
        IsPaid: '',
      },
      tableData: [],
      deleteIndex: null,
      deleteInpatientID: null,
    };
  },
  created() {
    this.fetchInpatients();
  },
  methods: {
    openSearchDialog() {
      this.searchDialogVisible = true;
    },
    resetSearchForm() {
      this.searchForm = {
        InpatientID: '',
        PatientID: '',
        HospitalDate: '',
        DischargedDate: '',
        HospitalBed: '',
        AdmissionType: '',
        IsPaid: '',
      };
    },
    handleNewButtonClick() {
      if (this.activeTab === 'Inpatient') {
        this.$router.push('/NewInpatient');
      } else if (this.activeTab === 'Inpatient-ICU') {
        this.$router.push('/NewInpatientICU');
      }
    },
    //取得資料顯示在畫面上
    fetchInpatients() {
      axios
        .post(api.domain + '/Inpatient/InpatientList', {})
        .then((response) => {
          console.log('資料:', response.data);
          if (response.data && response.data.Data) {
            this.tableData = response.data.Data;
          } else {
            console.error('Unexpected response structure:', response);
          }
        })
        .catch((error) => {
          console.error('Error fetching appointments:', error);
        });
    },
    //搜尋-視窗上的搜尋按鈕
    searchInpatients() {
      // Implement search logic here
      console.log('Search:', this.searchForm);
      this.searchDialogVisible = false;
    },
    //搜尋功能
    searchInpatient() {
      // 格式化 HospitalDate 為 'YYYY-MM-DD HH:mm:ss'
      const formattedHospitalDate = this.searchForm.HospitalDate
        ? dayjs(this.searchForm.HospitalDate).format('YYYY-MM-DD HH:mm:ss')
        : ''; // 如果日期為空，傳遞空字符串

      axios
        .post(api.domain + '/Inpatient/InpatientList', {
          InpatientID: this.searchForm.InpatientID,
          PatientID: this.searchForm.PatientID,
          HospitalDate: formattedHospitalDate, // 傳遞格式化的日期
          HospitalBed: this.searchForm.HospitalBed,
          AdmissionType: this.searchForm.AdmissionType,
        })
        .then((response) => {
          console.log('Response data:', response.data);
          if (response.data && response.data.Data) {
            this.tableData = response.data.Data;
            this.searchDialogVisible = false;
          } else {
            console.error('Unexpected response structure:', response);
          }
        })
        .catch((error) => {
          console.error('Error fetching appointments:', error);
        });
    },
    //確認刪除視窗
    confirmDelete(index, InpatientID) {
      this.deleteIndex = index;
      this.deleteInpatientID = InpatientID;
      this.showDeleteModal(() => this.handleDelete());
    },
    //刪除資料 Inpatient
    handleDelete() {
      axios
        .post(api.domain + '/Inpatient/DeleteInpatient', {
          InpatientID: this.deleteInpatientID,
        })
        .then((response) => {
          console.log('刪除回應:', response.data);
          this.tableData.splice(this.deleteIndex, 1);
        })
        .catch((error) => {
          console.error('刪除預約時出錯:', error);
        });
    },
    //刪除視窗
    showDeleteModal(onConfirm) {
      console.log('showDeleteModal 已被啟用');
      if (this.$refs.deleteConfirmation && this.$refs.deleteConfirmation.showDeleteModal) {
        this.$refs.deleteConfirmation.showDeleteModal(onConfirm);
      } else {
        console.error('DeleteConfirmation component or method not found.');
      }
    },
    //資料傳遞Inpatients
    InpatientsEdit(row) {
        this.$router.push({ name: 'NewInpatient', query: { InpatientID: row.InpatientID } });
        console.log('Editing Inpatients with ID:', row.InpatientID);
    },
    //排序
    handleSortChange({ column, prop, order }) {
      console.log('Sort change:', column, prop, order);
      this.tableData.sort((a, b) => {
        if (order === 'ascending') {
          return a[prop] > b[prop] ? 1 : -1;
        } else {
          return a[prop] < b[prop] ? 1 : -1;
        }
      });
    },
    handleTabClick(tab) {
      console.log('Tab clicked:', tab);
    },
  },
};
</script>

  
  <style scoped>
  .header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px; /*按鈕跟欄位的間距 */
  }
  
  .card {
    background-color: #eaf5fc;
    border-radius: 30px; /*切角 */
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  }
  
  .el-table {
    border-radius: 20px; /*切角 */
  }
  
  .el-icon {
    margin-right: 10px; /* 修改跟刪除icon的距離 */
  }
  </style>