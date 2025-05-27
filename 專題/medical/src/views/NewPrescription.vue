<template>
  <div class="card">
    <div class="p">
      <el-button @click="showConfirmationDialog" class="back-button">
        <el-icon><Back /></el-icon> Back
      </el-button>
      
      <el-form :model="form" label-width="150px">
        <el-row :gutter="20">

          <el-col :span="11">
            <el-form-item label="Patient ID:">
              <el-input v-model="form.PatientID" placeholder="" />
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="Prescription ID:">
              <el-input v-model="form.PrescriptionID" placeholder="New" :disabled="true"/>
            </el-form-item>
          </el-col>

          <el-col :span="11">
            <el-form-item label="Prescription Date:">
              <el-date-picker
                v-model="form.PrescriptionDate"
                type="date"
                placeholder="Select Date"
                style="width: 100%;"
              />
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="Log In User:">
              <el-input v-model="form.LogInUser" placeholder="" />
            </el-form-item>
          </el-col>

          <el-col :span="11">
            <el-form-item label="Prescribing Doctor:">
              <el-input v-model="form.PrescribingDoctor" placeholder=""/>
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="Pharmacy:">
              <el-input v-model="form.Pharmacy" placeholder=""/>
            </el-form-item>
          </el-col>

          <el-col :span="11">
            <el-form-item label="Invoice exempt:">
              <el-input v-model="form.InvoiceExempt" placeholder=""/>
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="Invoice Status:">
              <el-input v-model="form.InvoiceStatus" placeholder="To be invoiced" :disabled="true"/>
            </el-form-item>
          </el-col>

          <el-col :span="11">
            <el-form-item label="Invoice:" >
              <el-input v-model="form.Invoice" placeholder="" :disabled="true"/>
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="Appointment:">
              <el-input v-model="form.Appointment" placeholder=""/>
            </el-form-item>
          </el-col>

          <!-- Prescription line -->
          <el-col :span="23">
            <el-form-item label="Prescription line">
              <el-table :data="form.Prescriptions" style="width: 100%">
                <el-table-column prop="Print" label="Print" width="80" sortable="custom">
                  <template #default="scope">
                    <el-select v-model="scope.row.Print" placeholder="">
                      <el-option label="Yes" value="Yes"></el-option>
                      <el-option label="No" value="No"></el-option>
                    </el-select>
                  </template>
                </el-table-column>
                
                <el-table-column prop="Medicament" label="Medicament" width="130" sortable="custom"></el-table-column>
                <el-table-column prop="LotNo" label="Lot No." width="100" sortable="custom"></el-table-column>
                <el-table-column prop="Indication" label="Indication" width="120" sortable="custom"></el-table-column>
                <el-table-column prop="Dose" label="Dose" width="90" sortable="custom"></el-table-column>
                <el-table-column prop="DoseUnit" label="dose unit" width="120" sortable="custom"></el-table-column>
                <el-table-column prop="Form" label="Form" width="90" sortable="custom"></el-table-column>
                <el-table-column prop="CommonDosage" label="Common Dosage" width="170" sortable="custom"></el-table-column>
                <el-table-column prop="Quantity" label="Quantity" width="110" sortable="custom"></el-table-column>
                
                <el-table-column label="Operations" width="100">
                  <template #default="scope">
                    <el-icon @click="PrescriptionEdit(scope.row)" size="small">
                      <Edit />
                    </el-icon>
                    <el-icon @click="confirmDeletePrescription(scope.$index, scope.row.SeqNo)" size="small">
                      <Delete />
                    </el-icon>
                  </template>
                </el-table-column>
              </el-table>
              <el-button type="text" @click="showPrescriptionDialog">NEW</el-button>

              <el-dialog title="Prescription line" v-model="isPrescriptionDialogVisible" width="85%" >
                <el-form :model="newPrescription" label-width="150px">
                  <el-row :gutter="25">
                    <!-- 第一行 -->
                    <el-col :span="12">
                      <el-form-item label="Medicament:" style="margin-bottom: 10px;">
                        <el-input v-model="newPrescription.Medicament" />
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="Indication:" style="margin-bottom: 10px;">
                        <el-input v-model="newPrescription.Indication" />
                      </el-form-item>
                    </el-col>
                    
                    <!-- 第二行 -->
                    <el-col :span="12">
                      <el-form-item label="Allow substitution:" style="margin-bottom: 10px;">
                        <el-checkbox v-model="newPrescription.AllowSubstitution" />
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="Print:" style="margin-bottom: 10px;">
                        <el-checkbox v-model="newPrescription.Print" />
                      </el-form-item>
                    </el-col>

                    <!-- 第三行 -->
                    <el-col :span="12">
                      <el-form-item label="Form:" style="margin-bottom: 10px;">
                        <el-input v-model="newPrescription.Form" />
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="Administration Route:" style="margin-bottom: 10px;">
                        <el-input v-model="newPrescription.AdministrationRoute" />
                      </el-form-item>
                    </el-col>

                    <!-- 第四行 -->
                    <el-col :span="12">
                      <el-form-item label="Start of treatment:" style="margin-bottom: 10px;">
                        <el-date-picker v-model="newPrescription.StartTreatment" type="date" style="width: 100%;" />
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="End of treatment:" style="margin-bottom: 10px;">
                        <el-date-picker v-model="newPrescription.EndTreatment" type="date" style="width: 100%;" />
                      </el-form-item>
                    </el-col>
                    
                    <!-- 第五行 -->
                    <el-col :span="24">
                      <el-form-item label="Lot No.:" style="margin-bottom: 30px;">
                        <el-input v-model="newPrescription.LotNo" />
                      </el-form-item>
                    </el-col>

                    <!-- 分隔線 -->
                    <el-col :span="24">
                      <el-divider class="left-align-divider"><strong>DOSAGE</strong></el-divider>
                    </el-col>
                    
                    <!-- 第六行 -->
                    <el-col :span="8">
                      <el-form-item label="Dose:" style="margin-bottom: 30px;">
                        <el-input v-model="newPrescription.Dose" />
                      </el-form-item>
                    </el-col>
                    <el-col :span="8">
                      <el-form-item label="dose unit:" style="margin-bottom: 10px;">
                        <el-input v-model="newPrescription.DoseUnit" />
                      </el-form-item>
                    </el-col>
                    <el-col :span="8">
                      <el-form-item label="X:" style="margin-bottom: 30px;">
                        <el-input v-model="newPrescription.DoseX" />
                      </el-form-item>
                    </el-col>

                    <!-- 分隔線 -->
                    <el-col :span="24">
                      <el-divider class="left-align-divider"><strong>COMMON DOSAGE</strong></el-divider>
                    </el-col>

                    <!-- 第七行 -->
                    <el-col :span="12">
                      <el-form-item label="Common Dosage:" style="margin-bottom: 10px;">
                        <el-input v-model="newPrescription.CommonDosage" />
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="Admin hours:" style="margin-bottom: 30px;">
                        <el-input v-model="newPrescription.AdminHours" />
                      </el-form-item>
                    </el-col>

                    <!-- 分隔線 -->
                    <el-col :span="24">
                      <el-divider class="left-align-divider"><strong>SPECIFIC DOSAGE</strong></el-divider>
                    </el-col>

                    <!-- 第八行 -->
                    <el-col :span="12">
                      <el-form-item label="Frequency:" style="margin-bottom: 10px;">
                        <el-input v-model="newPrescription.Frequency" />
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="unit:" style="margin-bottom: 10px;">
                        <el-input v-model="newPrescription.Unit" />
                      </el-form-item>
                    </el-col>

                    <!-- 第九行 -->
                    <el-col :span="12">
                      <el-form-item label="Treatment duration:" style="margin-bottom: 10px;">
                        <el-input v-model="newPrescription.TreatmentDuration" />
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="Treatment Period:" style="margin-bottom: 10px;">
                        <el-input v-model="newPrescription.TreatmentPeriod" />
                      </el-form-item>
                    </el-col>

                    <!-- 第十行 -->
                    <el-col :span="12">
                      <el-form-item label="Review:" style="margin-bottom: 10px;">
                        <el-input v-model="newPrescription.Review" />
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="Quantity:" style="margin-bottom: 10px;">
                        <el-input v-model="newPrescription.Quantity" />
                      </el-form-item>
                    </el-col>

                    <!-- 第十一行 -->
                    <el-col :span="12">
                      <el-form-item label="Refills:" style="margin-bottom: 10px;">
                        <el-input v-model="newPrescription.Refills" />
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="Comment:" style="margin-bottom: 10px;">
                        <el-input v-model="newPrescription.Comment" />
                      </el-form-item>
                    </el-col>
                    
                  </el-row>
                </el-form>
                <div slot="footer" class="dialog-footer" style="margin-bottom: 10px;">
                  <el-button @click="isPrescriptionDialogVisible = false">Cancel</el-button>
                  <el-button type="primary" @click="savePrescription">Save</el-button>
                </div>
              </el-dialog>

            </el-form-item>
          </el-col>

          <!-- Notes -->
          <el-col :span="23">
            <el-form-item label="Notes:">
              <el-input type="textarea" v-model="form.Notes"/>
            </el-form-item>
          </el-col>
        </el-row>

        <!-- Action Buttons -->
        <el-form-item class="action-buttons">
          <el-button type="danger" @click="showDeleteModal">
            <el-icon><Delete /></el-icon> Delete
          </el-button>
          <el-button type="primary" @click="handleSubmit">
            <el-icon><DocumentChecked /></el-icon> Save
          </el-button>
        </el-form-item>


      </el-form>

      <DeleteConfirmation ref="deleteConfirmation" @confirmed-delete="handleDelete" />
    </div>
  </div>
  
</template>

  
<script>
  import { Back, DocumentChecked, Delete } from '@element-plus/icons-vue';
  import DeleteConfirmation from '../components/DeleteConfirmation.vue';
  import * as api from '../api/api.js';
  import Swal from 'sweetalert2';
  import axios from 'axios';

  export default {
    name: 'NewPrescription',
    components: {
      Back,
      DocumentChecked,
      Delete,
      DeleteConfirmation
    },
    data() {
      return {
        form: {
          "PatientID": '',
          "PrescriptionID": '',
          "PrescriptionDate": '',
          "LogInUser": '',
          "PrescribingDoctor": '',
          "Pharmacy": '',
          "InvoiceExempt": '',
          "InvoiceStatus": '',
          "Invoice": '',
          "Appointment": '',
          "Note": '',
          "Prescription line": [
            {
              "Print": '',
              "Medicament": '',
              "LotNo": '',
              "Indication": '',
              "Dose": '',
              "DoseUnit": '',
              "Form": '',
              "CommonDosage": '',
              "Quantity": ''
            }
          ],
          Prescriptions: [],
        },
        isPrescriptionDialogVisible: false,
        newPrescription: {
          Medicament: '',
          Indication: '',
          AllowSubstitution: false,
          Print: false,
          Form: '',
          AdministrationRoute: '',
          StartTreatment: '',
          EndTreatment: '',
          LotNo: '',
          Dose: '',
          DoseUnit: '',
          DoseX: '',
          CommonDosage: '',
          AdminHours: '',
          Frequency: '',
          Unit: '',
          TreatmentDuration: '',
          TreatmentPeriod: '',
          Review: '',
          Quantity: '',
          Refills: '',
          Comment: ''
        }
      };
    },
    created() {
      
    },
    methods: {
      // 顯示確認視窗
      showConfirmationDialog() {
        this.$refs.deleteConfirmation.showBackConfirmationModal();
      },
      confirmDelete(index, SeqNo) {
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
      showPrescriptionDialog() {
        console.log('Dialog visibility before:', this.isPrescriptionDialogVisible);
        this.isPrescriptionDialogVisible = true;
        console.log('Dialog visibility after:', this.isPrescriptionDialogVisible);
      },
      savePrescription() {
        this.form.Prescriptions.push({...this.newPrescription});
        this.isPrescriptionDialogVisible = false;
        // 重置 newPrescription 表單字段
        this.newPrescription = {
          Medicament: '',
          LotNo: '',
          Indication: '',
          Dose: '',
          DoseUnit: '',
          Form: '',
          CommonDosage: '',
          Quantity: ''
        };
      },
      // 刪除資料
      handleDelete() {
        
      },
      showDeleteModal() {
        this.$refs.deleteConfirmation.showDeleteModal();
      },
      
    }
  };
</script>
  
<style scoped>
  .card {
    background-color: #eaf5fc;
    border-radius: 30px;
    padding: 15px;
    width: auto;
    box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.1);
  }
  .p {
    background-color: #ffffff;
    border-radius: 30px;
  }
  .el-form-item {
    margin-left: 50px;
    margin-bottom: 12px;
    right: 70%;
  }
  .el-button {
    margin-top: 20px;
    margin-left: 1%;
  }
  .action-buttons {
    margin-left: 69%;
  }
  .flex-container {
    display: flex;
    gap: 10px; /* Adjust gap between the select elements as needed */
  }
  .el-icon {
  margin-right: 10px; /* 修改跟刪除icon的距離 */
  }
  .custom-row .el-form-item {
  margin-bottom: 20px; /* 調整這個值來改變全局的間距 */
}
.bold-divider {
  font-weight: bold;
}
.left-align-divider {
  text-align: left;
}
  
</style>
  