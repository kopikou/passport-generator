<template>
  <div class="indicator-disciplines-section">
    <div class="text-h5 q-mb-sm">{{ sectionTitle }}</div>
    <div class="section-details">
      <div class="text-subtitle1 text-grey">Индикаторы и их содержание автоматически получены из учебного плана.</div>
      <q-card flat bordered class="q-pa-md">
        <div class="text-body1 text-grey">
          Раздел находится в разработке...
        </div>
      </q-card>
    </div>
  </div>
</template>

<script setup>
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

const sectionTitle = '2.1. Соотнесение индикаторов достижения компетенций с дисциплинами (модулями), практиками'
</script>

<style scoped lang="scss">
.indicator-disciplines-section {
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