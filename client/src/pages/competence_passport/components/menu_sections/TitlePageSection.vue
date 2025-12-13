<template>
  <div class="title-page-section">
    <div class="text-h5 q-mb-sm">{{ sectionTitle }}</div>
    <div class="q-gutter-y-sm">
      <div v-if="planData?.admission?.cadmkind != 5">
        <div class="text-subtitle1 q-mb-xs">Профиль/Специальность</div>
        <q-field outlined dense>
          <template v-slot:control>
            <div class="self-center full-width no-outline">{{ planData?.admission?.spec_name }}</div>
          </template>
        </q-field>
      </div>
      
      <div v-if="planData?.admission?.cadmkind != 5">
        <div class="text-subtitle1 q-mb-xs">Наименование направления</div>
        <q-field outlined dense>
          <template v-slot:control>
            <div class="self-center full-width no-outline">{{ planData?.admission?.direct_name }}</div>
          </template>
        </q-field>
      </div>
      
      <div v-if="planData?.admission?.cadmkind == 5">
        <div class="text-subtitle1 q-mb-xs">Наименование направления</div>
        <q-field outlined dense>
          <template v-slot:control>
            <div class="self-center full-width no-outline">{{ getSpecName(planData?.admission?.spec_name) }}</div>
          </template>
        </q-field>
      </div>
      
      <div v-if="planData?.admission?.cadmkind == 5">
        <div class="text-subtitle1 q-mb-xs">Направленность</div>
        <q-field outlined dense>
          <template v-slot:control>
            <div class="self-center full-width no-outline">{{ getSpecNapr(planData?.admission?.spec_name) }}</div>
          </template>
        </q-field>
      </div>
      
      <div>
        <div class="text-subtitle1 q-mb-xs">Факультет</div>
        <q-field outlined dense>
          <template v-slot:control>
            <div class="self-center full-width no-outline">{{ planData?.admission?.cfac__name }}</div>
          </template>
        </q-field>
      </div>
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

const sectionTitle = 'Титульный лист'

const getSpecNapr = (name) => {
  if (!name) return 'Отсутствует'
  const names = name.split("направленность")
  if (names.length > 1) {
    return names[1].replace(' - ', '')
  } else {
    return 'Отсутствует'
  }
}

const getSpecName = (name) => {
  if (!name) return ''
  const names = name.split("направленность")
  if (names.length > 1) {
    return names[0].replace(', ', '')
  } else {
    return name
  }
}
</script>

<style scoped lang="scss">
.title-page-section {
  .q-field {
    margin-bottom: 12px;
    
    &:last-child {
      margin-bottom: 0;
    }
    
    .q-field__control {
      background: #f5f5f5;
      min-height: 40px;
    }
  }
}
</style>