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
        <el-tab-pane label="Patients" name="patients">
          <el-table :data="tableData" style="width: 100%" @sort-change="handleSortChange">
            <el-table-column prop="PatientID" label="Patient ID" width="150" sortable="custom"></el-table-column>
            <el-table-column prop="PatientName" label="Patient Name" width="150" sortable="custom"></el-table-column>
            <el-table-column prop="Sex" label="Sex" width="90" sortable="custom"></el-table-column>
            <el-table-column prop="Age" label="Age" width="90" sortable="custom"></el-table-column>
            <el-table-column prop="Birthday" label="Date of Birth" width="180" sortable="custom"></el-table-column>
            <el-table-column prop="HospitalStatus" label="Hospitalization Status" width="200" sortable="custom"></el-table-column>
            <el-table-column prop="DoctorName" label="Primary Care Doctor" width="190" sortable="custom"></el-table-column>
            <el-table-column label="Operations" width="145">
              <template #default="scope">
                <el-icon @click="PatientsEdit(scope.row)" size="small">
                  <Edit />
                </el-icon>
                <el-icon @click="confirmDelete(scope.$index, scope.row.PatientID)" size="small">
                  <Delete />
                </el-icon>
              </template>
            </el-table-column>
          </el-table>
          <!-- 搜尋對話框 Patients -->
          <el-dialog title="Patients" v-model="searchDialogVisible" width="50%">
            <el-form :model="searchForm" label-width="170px">
              <el-form-item label="Patient ID:">
                <el-input v-model="searchForm.PatientID" placeholder="Please enter a Patient ID"></el-input>
              </el-form-item>
              <el-form-item label="Patient Name:">
                <el-input v-model="searchForm.PatientName" placeholder="Please enter a Patient Name"></el-input>
              </el-form-item>
              <el-form-item label="Hospitalization Status:">
                <el-input v-model="searchForm.HospitalStatus" placeholder="Please enter a Hospitalization Status"></el-input>
              </el-form-item>
              <el-form-item label="Primary Care Doctor:">
                <el-input v-model="searchForm.Doctor" placeholder="Please enter a Doctor"></el-input>
              </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
              <el-button @click="resetSearchForm">Reset</el-button>
              <el-button type="primary" @click="searchPatients">Search</el-button>
            </span>
          </el-dialog>
        </el-tab-pane>

        <el-tab-pane label="Families" name="families">
          <el-table :data="familyData" style="width: 100%" @sort-change="handleSortChangeFamilies">
            <el-table-column prop="FamilyName" label="FamilyName" width="140" sortable="custom"></el-table-column>
            <el-table-column prop="Relationship" label="Relationship" width="150" sortable="custom"></el-table-column>
            <el-table-column prop="PatientID" label="Patient ID" width="150" sortable="custom"></el-table-column>
            <el-table-column prop="PhoneNo" label="Phone No" width="150" sortable="custom"></el-table-column>
            <el-table-column prop="Tel" label="TEL" width="110" sortable="custom"></el-table-column>
            <el-table-column prop="Company" label="Company" width="150" sortable="custom"></el-table-column>
            <el-table-column label="Operations" width="145">
              <template #default="scope">
                <el-icon @click="FamilyEdit(scope.row)" size="small">
                  <Edit />
                </el-icon>
                <el-icon @click="confirmDeleteFamily(scope.$index, scope.row.SeqNo)" size="small">
                  <Delete />
                </el-icon>
              </template>
            </el-table-column>
          </el-table>

          <!-- 搜尋對話框 Families -->
          <el-dialog title="Families" v-model="searchDialogVisible" width="50%">
            <el-form :model="searchForm" label-width="140px">
              <el-form-item label="Name:">
                <el-input v-model="searchForm.Name" placeholder="Please enter a Name"></el-input>
              </el-form-item>
              <el-form-item label="Patient ID:">
                <el-input v-model="searchForm.PatientID" placeholder="Please enter a Patient ID"></el-input>
              </el-form-item>
              <el-form-item label="TEL:">
                <el-input v-model="searchForm.TEL" placeholder="Please enter a TEL"></el-input>
              </el-form-item>
              <el-form-item label="Phone No:">
                <el-input v-model="searchForm.PhoneNo" placeholder="Please enter a Phone No"></el-input>
              </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
              <el-button @click="resetSearchForm">Reset</el-button>
              <el-button type="primary" @click="searchFamily">Search</el-button>
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
import * as api from '../api/api.js';
import axios from 'axios';

export default {
  name: 'Patients',
  components: {
    Edit,
    Delete,
    Plus,
    Search,
    DeleteConfirmation,
  },
  data() {
    return {
      activeTab: 'patients',
      searchDialogVisible: false,
      searchForm: {
        PatientID: '',
        PatientName: '',
        Sex: '',
        Age: '',
        Birthday: '',
        HospitalStatus: '',
        Doctor: '',
      },
      tableData: [],
      familyData: [],
      deleteIndex: null,
      deletePatientID: null,
      deleteSeqNo: null,
    };
  },
  created() {
    this.fetchPatients();
    this.fetchFamily(); 
  },
  methods: {
  openSearchDialog() {
    this.searchDialogVisible = true;
  },
  resetSearchForm() {
    this.searchForm = {
      PatientID: '',
      PatientName: '',
      HospitalStatus: '',
      Doctor: '',
    };
  },
  //搜尋功能-Patients
  searchPatients() {
    const { PatientID, PatientName, HospitalStatus, Doctor } = this.searchForm;
    axios
      .post(api.domain + '/Patient/PatientList', {
        PatientID: PatientID,
        PatientName: PatientName,
        HospitalStatus: HospitalStatus,
        Doctor: Doctor,
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
  //搜尋功能-Family
  searchFamily() {
      const { Name, PatientID, TEL, PhoneNo } = this.searchForm;
      axios
        .post(api.domain + '/Family/FamilyList', {
          FamilyName: Name,
          PatientID: PatientID,
          Tel: TEL,
          PhoneNo: PhoneNo,
        })
        .then((response) => {
          console.log('Response data:', response.data);
          if (response.data && response.data.Data) {
            this.familyData = response.data.Data; // 將結果賦值給 familyData
            this.searchDialogVisible = false;
          } else {
            console.error('Unexpected response structure:', response);
          }
        })
        .catch((error) => {
          console.error('Error fetching appointments:', error);
        });
  },
  //取得資料-Patient
  fetchPatients() {
    axios
      .post(api.domain + '/Patient/PatientList', {})
      .then((response) => {
        console.log('Response data:', response.data);
        if (response.data && response.data.Data) {
          this.tableData = response.data.Data;
          console.log(this.tableData); // 檢查返回的資料結構
        } else {
          console.error('Unexpected response structure:', response);
        }
      })
      .catch((error) => {
        console.error('Error fetching PatientList:', error);
      });
  },
  //取得資料-Family
  fetchFamily() {
    axios
      .post(api.domain + '/Family/FamilyList', {})
      .then((response) => {
        console.log('Response 資料:', response.data);
        if (response.data && response.data.Data) {
          this.familyData = response.data.Data;
          console.log(this.familyData); // 檢查返回的資料結構
        } else {
          console.error('Unexpected response structure:', response);
        }
      })
      .catch((error) => {
        console.error('Error fetching FamilyList:', error);
      });
  },
  handleNewButtonClick() {
      if (this.activeTab === 'patients') {
        this.$router.push('/NewPatients');
      } else if (this.activeTab === 'families') {
        this.$router.push('/NewFamily');
      }
  },
  //資料傳遞Patients
  PatientsEdit(row) {
      this.$router.push({ name: 'NewPatients', query: { patientID: row.PatientID } });
      console.log('Editing Patients with ID:', row.PatientID);
  },
  //資料傳遞Family
  FamilyEdit(row) {
    this.$router.push({ name: 'NewFamily', query: { seqNo: row.SeqNo } });
    console.log('Editing family with SeqNo:', row.SeqNo);
  },
  //跳轉資料欄位時，New按鈕的轉換
  handleEdit(index, row) {
    this.$router.push({ 
      path: '/Family', 
    });
  },
  //刪除確認視窗
  confirmDelete(index, PatientID) {
    this.deleteIndex = index;
    this.deletePatientID = PatientID;
    this.showDeleteModal(() => this.handleDelete());
  },
  confirmDeleteFamily(index, SeqNo) {
    this.deleteIndex = index;
    this.deleteSeqNo = SeqNo;
    this.showDeleteModal(() => this.handleDeleteFamily());
  },
  showDeleteModal(onConfirm) {
    console.log('showDeleteModal 已被啟用');
    if (this.$refs.deleteConfirmation && this.$refs.deleteConfirmation.showDeleteModal) {
      this.$refs.deleteConfirmation.showDeleteModal(onConfirm);
    } else {
      console.error('DeleteConfirmation component or method not found.');
    }
  },
  // 刪除資料 Patient
  handleDelete() {
    axios
      .post(api.domain + '/Patient/DeletePatient', {
        PatientID: this.deletePatientID,
      })
      .then((response) => {
        console.log('刪除回應:', response.data);
        this.tableData.splice(this.deleteIndex, 1);
      })
      .catch((error) => {
        console.error('刪除預約時出錯:', error);
      });
  },
  // 刪除資料 Family
  handleDeleteFamily() {
    axios
      .post(api.domain + '/Family/DeleteFamily', {
        SeqNo: this.deleteSeqNo,
      })
      .then((response) => {
        console.log('刪除回應:', response.data);
        this.familyData.splice(this.deleteIndex, 1);
      })
      .catch((error) => {
        console.error('刪除預約時出錯:', error);
      });
  },
  //資料排序-Patients
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
  //資料排序-Families
  handleSortChangeFamilies({ column, prop, order }) {
    console.log('Sort change:', column, prop, order);
    this.familyData.sort((a, b) => {
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
@media (min-width: 720px){}


@media (max-width: 1024px) {}

@media (min-width: 1024px) {}

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px; /* 按鈕跟欄位的間距 */
}

.card {
  background-color: #eaf5fc;
  border-radius: 30px; /* 切角 */
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.el-table {
  border-radius: 20px; /*切角 */
}

.el-icon {
  margin-right: 10px; /* 修改跟刪除icon的距離 */
}
</style>
