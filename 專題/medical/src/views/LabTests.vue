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
        
        <!-- Multiple Tests Wizard 頁面 -->
        <el-tabs v-model="activeTab" @tab-click="handleTabClick">
          <el-tab-pane label="Multiple Tests Wizard" name="multipleTests">
            <el-table :data="multipleTestsData" style="width: 100%" @sort-change="handleSortChange">
              <el-table-column prop="RequestDate" label="Request Date" width="170" sortable="custom"></el-table-column>
              <el-table-column prop="PatientID" label="Patient ID" width="150" sortable="custom"></el-table-column>
              <el-table-column prop="Doctor" label="Doctor" width="150" sortable="custom"></el-table-column>
              <el-table-column prop="Urgent" label="Urgent" width="150" sortable="custom"></el-table-column>
              <el-table-column prop="Jost" label="Jost" width="150" sortable="custom"></el-table-column>
              <el-table-column prop="Code" label="Code" width="150" sortable="custom"></el-table-column>
              <el-table-column label="Operations" width="145">
                <template #default="scope">
                  <el-icon @click="editTest(scope.row)" size="small">
                    <Edit />
                  </el-icon>
                  <el-icon @click="confirmDelete(scope.$index, scope.row.TestID)" size="small">
                    <Delete />
                  </el-icon>
                </template>
              </el-table-column>
            </el-table>
            <!-- 搜尋對話框 Multiple Tests Wizard -->
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

          <!-- Lab Tests Results 頁面 -->
          <el-tab-pane label="Lab Tests Results" name="labTestsResults">
            <el-table :data="multipleTestsData" style="width: 100%" @sort-change="handleSortChange">
              <el-table-column prop="LabID" label="Lab ID" width="150" sortable="custom"></el-table-column>
              <el-table-column prop="Testtype" label="Test Type" width="150" sortable="custom"></el-table-column>
              <el-table-column prop="PatientID" label="Patient ID" width="150" sortable="custom"></el-table-column>
              <el-table-column prop="DateoftheAnalysis" label="Date of the Analysis" width="230" sortable="custom"></el-table-column>
              <el-table-column label="Operations" width="145">
                <template #default="scope">
                  <el-icon @click="editTest(scope.row)" size="small">
                    <Edit />
                  </el-icon>
                  <el-icon @click="confirmDelete(scope.$index, scope.row.TestID)" size="small">
                    <Delete />
                  </el-icon>
                </template>
              </el-table-column>
            </el-table>
            <!-- 搜尋對話框 Lab Tests Results -->
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
  

          <!-- Lab Request 頁面 -->
          <el-tab-pane label="Lab Request" name="labRequest">
            <el-table :data="multipleTestsData" style="width: 100%" @sort-change="handleSortChange">
              <el-table-column prop="RequestID" label="Request ID" width="150" sortable="custom"></el-table-column>
              <el-table-column prop="Testtype" label="Test Type" width="150" sortable="custom"></el-table-column>
              <el-table-column prop="Date" label="Date" width="130" sortable="custom"></el-table-column>
              <el-table-column prop="PatientID" label="Patient ID" width="150" sortable="custom"></el-table-column>
              <el-table-column prop="Doctor" label="Doctor" width="150" sortable="custom"></el-table-column>
              <el-table-column prop="State" label="State" width="150" sortable="custom"></el-table-column>
              <el-table-column prop="Urgent" label="Urgent" width="150" sortable="custom"></el-table-column>
              <el-table-column label="Operations" width="145">
                <template #default="scope">
                  <el-icon @click="editTest(scope.row)" size="small">
                    <Edit />
                  </el-icon>
                  <el-icon @click="confirmDelete(scope.$index, scope.row.TestID)" size="small">
                    <Delete />
                  </el-icon>
                </template>
              </el-table-column>
            </el-table>
            <!-- 搜尋對話框 Lab Request -->
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
  
      
      <!-- Delete Confirmation Component -->
      <DeleteConfirmation ref="deleteConfirmation" />
    </div>
  </template>
  
  <script>
import { Edit, Delete, Plus, Search } from '@element-plus/icons-vue';
import DeleteConfirmation from '../components/DeleteConfirmation.vue';
import * as api from '../api/api.js';
import axios from 'axios';

export default {
  name: 'LabTests',
  components: {
    Edit,
    Delete,
    Plus,
    Search,
    DeleteConfirmation,
  },
  data() {
    return {
      activeTab: 'multipleTests',
      searchDialogVisible: false,
      searchForm: {}, // 對應不同頁籤的表單資料
      multipleTestsData: [], // 資料
    };
  },
  methods: {
    openSearchDialog() {
      this.searchDialogVisible = true;
    },
    resetSearchForm() {
      this.searchForm = {}; // 重置表單
    },
    handleNewButtonClick() {
      if (this.activeTab === 'multipleTests') {
        this.$router.push('/NewLabTest');
      } else if (this.activeTab === 'labTestsResults') {
        this.$router.push('/NewLabTestResults');
      } else if (this.activeTab === 'labRequest') {
        this.$router.push('/NewLabRequest');
      }
    },
    handleTabClick(tab) {
      this.activeTab = tab.name; // 更新當前選中的頁籤
    },
    searchTests() {
      // 根據不同的頁籤執行不同的搜尋邏輯
      if (this.activeTab === 'multipleTests') {
        // 執行 Multiple Tests 的搜尋邏輯
      } else if (this.activeTab === 'labTestsResults') {
        // 執行 Lab Tests Results 的搜尋邏輯
      } else if (this.activeTab === 'labRequest') {
        // 執行 Lab Request 的搜尋邏輯
      }
      this.searchDialogVisible = false;
    },
  },
};
</script>
  
  <style scoped>
  .header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
  }
  .card {
    background-color: #eaf5fc;
    border-radius: 30px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  }
  .el-table {
    border-radius: 20px;
  }
  .el-icon {
    margin-right: 10px;
  }
  </style>
  