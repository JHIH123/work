<template>
  <div>
    <!-- 這裡不需要顯示任何按鈕，因為它將由父組件觸發 -->
  </div>
</template>

<script>
import Swal from 'sweetalert2';

export default {
  name: 'DeleteConfirmation',
  methods: {
    // 刪除視窗
    showDeleteModal(onConfirm) {
      Swal.fire({
        title: 'Do you really want to delete these records?',
        text: 'This process cannot be undone.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        cancelButtonText: 'Cancel',
        confirmButtonText: 'Delete',
      }).then((result) => {
        if (result.isConfirmed) {
          if (typeof onConfirm === 'function') {
            onConfirm(); // 調用回調函數
          } else {
            console.error('onConfirm is not a function');
          }
          Swal.fire({
            title: 'The record has been deleted.',
            icon: 'success',
            confirmButtonText: 'Close',
          })
        }
      });
    },
    //返回通知視窗
    showBackConfirmationModal() {
      Swal.fire({
        title: 'Are you sure?',
        text: 'Upon exit, records will not be saved.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        cancelButtonText: 'Cancel',
        confirmButtonText: "Yes, I'm sure"
      }).then((result) => {
        if (result.isConfirmed) {
          // 向父組件傳遞返回確認事件
          this.$router.back();
        }
      });
    }
  }
};
</script>

<style scoped>
/* 添加必要的樣式 */
</style>
