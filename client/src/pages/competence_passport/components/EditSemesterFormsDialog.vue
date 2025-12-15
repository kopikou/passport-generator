<template>
  <q-dialog v-model="showDialog" persistent>
    <q-card style="min-width: 500px;">
      <q-card-section>
        <div class="text-h6">Редактирование форм аттестации</div>
        <div class="text-subtitle2 text-grey q-mb-md">
          {{ editingData.competence_index }} - {{ editingData.competence }}
          <br>
          {{ editingData.discipline_index }} {{ editingData.discipline_name }}
          <br>
          Семестр: {{ editingData.semester }}
        </div>
      </q-card-section>

      <q-card-section>
        <div class="row items-center q-mb-md">
          <div class="col">
            <div class="text-subtitle2 text-grey">
              Выберите формы аттестации для семестра
            </div>
          </div>
          <div class="col-auto">
            <q-badge color="positive" outline>
              Выбрано: {{ selectedCount }}
            </q-badge>
            <q-badge color="grey" outline class="q-ml-sm">
              Всего: {{ allForms.length }}
            </q-badge>
          </div>
        </div>

        <!-- Переключатели форм аттестации -->
        <div class="q-gutter-y-md">
          <div class="row items-center">
            <div class="col-3">
              <q-toggle
                v-model="forms.ekz"
                color="positive"
                size="lg"
                label-color="dark"
              />
            </div>
            <div class="col">
              <div class="text-body2">Экзамен (Э)</div>
            </div>
          </div>

          <q-separator />

          <div class="row items-center">
            <div class="col-3">
              <q-toggle
                v-model="forms.zach"
                color="positive"
                size="lg"
                label-color="dark"
              />
            </div>
            <div class="col">
              <div class="text-body2">Зачет (З)</div>
            </div>
          </div>

          <q-separator />

          <div class="row items-center">
            <div class="col-3">
              <q-toggle
                v-model="forms.zacho"
                color="positive"
                size="lg"
                label-color="dark"
              />
            </div>
            <div class="col">
              <div class="text-body2">Зачет с оценкой (Зо)</div>
            </div>
          </div>

          <q-separator />

          <div class="row items-center">
            <div class="col-3">
              <q-toggle
                v-model="forms.kp"
                color="positive"
                size="lg"
                label-color="dark"
              />
            </div>
            <div class="col">
              <div class="text-body2">Курсовой проект (КП)</div>
            </div>
          </div>

          <q-separator />

          <div class="row items-center">
            <div class="col-3">
              <q-toggle
                v-model="forms.kr"
                color="positive"
                size="lg"
                label-color="dark"
              />
            </div>
            <div class="col">
              <div class="text-body2">Курсовая работа (КР)</div>
            </div>
          </div>
        </div>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="Закрыть" color="negative" @click="closeDialog" />
        <q-btn 
          label="Сохранить" 
          color="positive" 
          @click="saveForms" 
          :loading="store.saving"
          :disable="!hasChanges"
        >
          <q-tooltip v-if="!hasChanges">
            Нет изменений для сохранения
          </q-tooltip>
        </q-btn>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { useCompetencePassportStore } from 'stores/competencePassportStore'

const props = defineProps({
  modelValue: Boolean,
  editingData: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue', 'saved'])

const store = useCompetencePassportStore()
const showDialog = ref(false)
const forms = ref({
  ekz: false,
  zach: false,
  zacho: false,
  kp: false,
  kr: false
})

const originalForms = ref({})

const allForms = computed(() => [
  { key: 'ekz', label: 'Экзамен', short: 'Э' },
  { key: 'zach', label: 'Зачет', short: 'З' },
  { key: 'zacho', label: 'Зачет с оценкой', short: 'Зо' },
  { key: 'kp', label: 'Курсовой проект', short: 'КП' },
  { key: 'kr', label: 'Курсовая работа', short: 'КР' }
])

const selectedCount = computed(() => {
  return Object.values(forms.value).filter(value => value).length
})

const hasChanges = computed(() => {
  return JSON.stringify(forms.value) !== JSON.stringify(originalForms.value)
})

watch(() => props.modelValue, (val) => {
  showDialog.value = val
})

watch(showDialog, (val) => {
  emit('update:modelValue', val)
})

watch(() => props.editingData, (data) => {
  if (data.forms) {
    const newForms = {
      ekz: data.forms.includes('Э'),
      zach: data.forms.includes('З'),
      zacho: data.forms.includes('Зо'),
      kp: data.forms.includes('КП'),
      kr: data.forms.includes('КР')
    }
    forms.value = newForms
    originalForms.value = { ...newForms }
  }
}, { deep: true, immediate: true })

function closeDialog() {
  showDialog.value = false
  if (originalForms.value) {
    forms.value = { ...originalForms.value }
  } else {
    forms.value = {
      ekz: false,
      zach: false,
      zacho: false,
      kp: false,
      kr: false
    }
  }
}

async function saveForms() {
  try {
    const payload = {
      plan_id: props.editingData.planId || store.currentPlanId,
      discipline_id: props.editingData.discipline_id,
      competence_index: props.editingData.competence_index,
      semester: props.editingData.semester,
      forms: forms.value
    }

    await store.updateSemesterScheme(payload)
    
    originalForms.value = { ...forms.value }
    
    emit('saved')
    closeDialog()
  } catch (error) {
    console.error('Error saving forms:', error)
  }
}
</script>

<style scoped>
.row {
  align-items: center;
}
</style>