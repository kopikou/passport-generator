<template>
  <div class="competence-indicators-section">
    <div class="text-h5 q-mb-sm">{{ sectionTitle }}</div>
    <div class="section-details">
      <div class="text-subtitle1 text-grey">Раскройте для заполнения</div>
      <q-card flat bordered class="q-pa-md">
        <div class="text-body1 text-grey">
          Раздел находится в разработке...
        </div>
      </q-card>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  planData: {
    type: Object,
    default: () => ({})
  },
  competence: {
    type: Object,
    default: null
  },
  planId: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['data-saved'])

const sectionTitle = '3. Критерии и средства (методы) оценивания индикаторов достижения  компетенции в рамках промежуточной аттестации'
</script>

<style scoped lang="scss">
.competence-indicators-section {
  .section-details {
    margin-top: 16px;
    
    .text-subtitle1 {
      margin-bottom: 8px;
    }
    
    .q-card {
      min-height: 100px;
      margin-top: 8px;
    }
  }
}
</style>