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
        <el-table :data="tableData" style="width: 100%" @sort-change="handleSortChange">
          <el-table-column prop="PrescriptionID" label="Prescription ID" width="150" sortable="custom"></el-table-column>
          <el-table-column prop="PatientID" label="Patient ID" width="140" sortable="custom"></el-table-column>
          <el-table-column prop="LogInUser" label="Log In User" width="150" sortable="custom"></el-table-column>
          <el-table-column prop="PrescriptionDate" label="Prescription Date" width="180" sortable="custom"></el-table-column>
          <el-table-column prop="InvoiceExempt" label="Invoice exempt" width="150" sortable="custom"></el-table-column>
          <el-table-column prop="InvoiceStatus" label="Invoice Status" width="170" sortable="custom"></el-table-column>
          <el-table-column label="Operations" width="145">
            <template #default="scope">
              <el-icon @click="PrescriptionEdit(scope.row)" size="small">
                <Edit />
              </el-icon>
              <el-icon @click="confirmDelete(scope.$index, scope.row.PrescriptionID)" size="small">
                <Delete />
              </el-icon>
            </template>
          </el-table-column>
        </el-table>
  
        <!-- 搜尋視窗 -->
        <el-dialog title="Search Prescriptions" v-model="searchDialogVisible" width="50%">
          <el-form :model="searchForm" label-width="170px">
            <el-form-item label="Prescription ID:">
              <el-input v-model="searchForm.PrescriptionID" placeholder="Please enter a Prescription ID"></el-input>
            </el-form-item>
            <el-form-item label="Patient ID:">
              <el-input v-model="searchForm.PatientID" placeholder="Please enter a Patient ID"></el-input>
            </el-form-item>
            <el-form-item label="Prescription Date:" >
                <el-date-picker
                    v-model="searchForm.PrescriptionDate"
                    type="date"
                    placeholder="Please select a Prescription Date"
                    format="YYYY/MM/DD"
                    value-format="YYYY-MM-DD"
                    style="width: 100%;"
                />
            </el-form-item>
            <el-form-item label="Invoice exempt:">
              <el-input v-model="searchForm.InvoiceExempt" placeholder="Please enter Invoice exempt status"></el-input>
            </el-form-item>
          </el-form>
          <span slot="footer" class="dialog-footer">
            <el-button @click="resetSearchForm">Reset</el-button>
            <el-button type="primary" @click="searchPrescription">Search</el-button>
          </span>
        </el-dialog>
      </el-card>
      <!-- 确保 DeleteConfirmation 组件已正确引用 -->
      <DeleteConfirmation ref="deleteConfirmation" />
    </div>
  </template>
  
  <script>
  import { Edit, Delete, Plus, Search } from '@element-plus/icons-vue';
  import DeleteConfirmation from '../components/DeleteConfirmation.vue';
  import * as api from '../api/api.js';
  import axios from 'axios';
  
  export default {
    name: 'Prescription',
    components: {
      Edit,
      Delete,
      Plus,
      Search,
      DeleteConfirmation,
    },
    data() {
      return {
        searchDialogVisible: false,
        searchForm: {
          PrescriptionID: '',
          PatientID: '',
          LogInUser: '',
          PrescriptionDate: '',
          InvoiceExempt: '',
        },
        tableData: [],
        deleteIndex: null,
        deletePrescriptionID: null,
      };
    },
    created() {
      this.fetchPrescription();
    },
    methods: {
      openSearchDialog() {
        this.searchDialogVisible = true;
      },
      resetSearchForm() {
        this.searchForm = {
          PrescriptionID: '',
          PatientID: '',
          LogInUser: '',
          PrescriptionDate: '',
          InvoiceExempt: '',
        };
      },
      handleNewButtonClick() {
        this.$router.push('/NewPrescription');
      },
      //取得資料顯示在畫面上
      fetchPrescription() {
        axios
          .post(api.domain + '/Prescription/PresMedicamentList', {})
          .then((response) => {
            console.log('Response data123:', response.data);
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
      searchPrescription() {
        const { PrescriptionID, PatientID, LogInUser, PrescriptionDate, InvoiceExempt } = this.searchForm;
        axios
          .post(api.domain + '/Prescription/PrescriptionList', {
            PrescriptionID,
            PatientID,
            LogInUser,
            PrescriptionDate,
            InvoiceExempt,
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
            console.error('Error fetching prescriptions:', error);
          });
      },
      confirmDelete(index, PrescriptionID) {
        this.deleteIndex = index;
        this.deletePrescriptionID = PrescriptionID;
        this.showDeleteModal(() => this.handleDelete());
      },
      handleDelete() {
        axios
          .post(api.domain + '/Prescription/DeletePrescription', {
            PrescriptionID: this.deletePrescriptionID,
          })
          .then((response) => {
            console.log('刪除回應:', response.data);
            this.tableData.splice(this.deleteIndex, 1);
          })
          .catch((error) => {
            console.error('刪除時出錯:', error);
          });
      },
      showDeleteModal(onConfirm) {
        if (this.$refs.deleteConfirmation && this.$refs.deleteConfirmation.showDeleteModal) {
          this.$refs.deleteConfirmation.showDeleteModal(onConfirm);
        } else {
          console.error('DeleteConfirmation component or method not found.');
        }
      },
      PrescriptionEdit(row) {
        this.$router.push({ name: 'NewPrescription', query: { PrescriptionID: row.PrescriptionID } });
      },
      handleSortChange({ column, prop, order }) {
        this.tableData.sort((a, b) => {
          if (order === 'ascending') {
            return a[prop] > b[prop] ? 1 : -1;
          } else {
            return a[prop] < b[prop] ? 1 : -1;
          }
        });
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
  