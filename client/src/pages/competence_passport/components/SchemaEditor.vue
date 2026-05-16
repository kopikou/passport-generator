<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useCompetencePassportStore } from 'src/stores/competencePassportStore'
import { storeToRefs } from 'pinia'
import { useQuasar } from 'quasar'

const $q = useQuasar()

const props = defineProps({
  modelValue: Boolean,
  editingData: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue', 'saved'])

const store = useCompetencePassportStore()
const {
  currentPlanId,
  saving
} = storeToRefs(store)

const showDialog = ref(false)
const forms = ref({
  ekz: false,
  zach: false,
  zacho: false,
  kp: false,
  kr: false
})
const errorMessage = ref('')

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

// Загрузка данных формы
watch(() => props.editingData, (data) => {
  if (!data || !data.forms) {
    forms.value = {
      ekz: false,
      zach: false,
      zacho: false,
      kp: false,
      kr: false
    }
  } else {
    forms.value = {
      ekz: data.forms.ekz || false,
      zach: data.forms.zach || false,
      zacho: data.forms.zacho || false,
      kp: data.forms.kp || false,
      kr: data.forms.kr || false
    }
  }
  originalForms.value = { ...forms.value }
  errorMessage.value = ''
}, { deep: true, immediate: true })

function closeDialog() {
  showDialog.value = false
  errorMessage.value = ''
  forms.value = { ...originalForms.value }
}

async function saveForms() {
  errorMessage.value = ''
  
  try {
    await store.updateSemesterScheme(
      props.editingData.planId || currentPlanId.value!,
      props.editingData.discipline_id,
      props.editingData.competence_index,
      props.editingData.competence,
      props.editingData.semester,
      forms.value
    )
    
    originalForms.value = { ...forms.value }
    emit('saved')
    closeDialog()

    $q.notify({
      type: 'positive',
      message: 'Формы аттестации успешно сохранены',
      position: 'top-right',
      timeout: 2000
    })
  } catch (error: any) {
  
    $q.notify({
      type: 'negative',
      position: 'top-right',
      message: 'Ошибка при сохранении: Форма аттестации недоступна в этом семестре',
      timeout: 5000
    })
  }
}
</script>

<template>
  <q-dialog v-model="showDialog" persistent>
    <q-card style="min-width: 500px;">
      <q-card-section>
        <div class="text-h6">Редактирование форм аттестации</div>
        <div class="text-subtitle2 text-grey q-mb-md">
          <span v-if="editingData.competence_index">{{ editingData.competence_index }} - {{ editingData.competence }}</span>
          <br v-if="editingData.competence_index">
          <span v-if="editingData.discipline_index">{{ editingData.discipline_index }} {{ editingData.discipline_name }}</span>
          <br v-if="editingData.discipline_index">
          <span v-if="editingData.semester">Семестр: {{ editingData.semester }}</span>
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
          <div v-for="form in allForms" :key="form.key" class="row items-center">
            <div class="col-3">
              <q-toggle
                v-model="forms[form.key]"
                color="positive"
                size="lg"
                label-color="dark"
                :disable="saving"
              />
            </div>
            <div class="col">
              <div class="text-body2">{{ form.label }} ({{ form.short }})</div>
            </div>
          </div>
        </div>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="Закрыть" color="negative" @click="closeDialog" :disable="saving" />
        <q-btn 
          label="Сохранить" 
          color="positive" 
          @click="saveForms" 
          :loading="saving"
          :disable="!hasChanges || saving"
        >
          <q-tooltip v-if="!hasChanges">
            Нет изменений для сохранения
          </q-tooltip>
        </q-btn>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<style scoped>
.row {
  align-items: center;
}
</style>