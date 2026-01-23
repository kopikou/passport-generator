<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({
  planData: {
    type: Object,
    default: () => ({})
  },
  admissionInfo: {
    type: Object,
    default: () => ({})
  },
  planId: {
    type: Number,
    required: true
  }
})

const sectionTitle = 'Титульный лист'

const isSpecialty = computed(() => {
  return props.admissionInfo?.cadmkind === 5
})

const specName = computed(() => {
  if (!props.admissionInfo?.spec_name) return ''
  
  const name = props.admissionInfo.spec_name
  const parts = name.split('направленность')
  
  if (parts.length > 1) {
    return parts[0].replace(', ', '').trim()
  }
  return name.trim()
})

const specDirection = computed(() => {
  if (!props.admissionInfo?.spec_name) return 'Отсутствует'
  
  const name = props.admissionInfo.spec_name
  const parts = name.split('направленность')
  
  if (parts.length > 1) {
    return parts[1].replace(' - ', '').trim() || 'Отсутствует'
  }
  return 'Отсутствует'
})

const facultyName = computed(() => {
  return props.admissionInfo?.cfac__name || 'Не указан'
})

const directionName = computed(() => {
  return props.admissionInfo?.direct_name || 'Не указано'
})
</script>

<template>
  <div class="title-page-section">
    <div class="text-h5 q-mb-sm">{{ sectionTitle }}</div>
    <div class="q-gutter-y-sm">
      <!-- Профиль/Специальность (для бакалавриата/магистратуры) -->
      <div v-if="!isSpecialty">
        <div class="text-subtitle1 q-mb-xs">Профиль/Специальность</div>
        <q-field outlined dense>
          <template v-slot:control>
            <div class="self-center full-width no-outline">
              {{ props.admissionInfo?.spec_name || 'Не указано' }}
            </div>
          </template>
        </q-field>
      </div>
      
      <!-- Наименование направления (для бакалавриата/магистратуры) -->
      <div v-if="!isSpecialty">
        <div class="text-subtitle1 q-mb-xs">Наименование направления</div>
        <q-field outlined dense>
          <template v-slot:control>
            <div class="self-center full-width no-outline">
              {{ directionName }}
            </div>
          </template>
        </q-field>
      </div>
      
      <!-- Наименование направления (для специалитета) -->
      <div v-if="isSpecialty">
        <div class="text-subtitle1 q-mb-xs">Наименование направления</div>
        <q-field outlined dense>
          <template v-slot:control>
            <div class="self-center full-width no-outline">
              {{ specName }}
            </div>
          </template>
        </q-field>
      </div>
      
      <!-- Направленность (для специалитета) -->
      <div v-if="isSpecialty">
        <div class="text-subtitle1 q-mb-xs">Направленность</div>
        <q-field outlined dense>
          <template v-slot:control>
            <div class="self-center full-width no-outline">
              {{ specDirection }}
            </div>
          </template>
        </q-field>
      </div>
      
      <!-- Факультет -->
      <div>
        <div class="text-subtitle1 q-mb-xs">Факультет</div>
        <q-field outlined dense>
          <template v-slot:control>
            <div class="self-center full-width no-outline">
              {{ facultyName }}
            </div>
          </template>
        </q-field>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.title-page-section {
  .q-field {
    margin-bottom: 12px;
    &:last-child {
      margin-bottom: 0;
    }
  }
}
</style>