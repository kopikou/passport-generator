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
        <div class="q-gutter-sm">
          <q-checkbox v-model="forms.ekz" label="Экзамен (Э)" />
          <q-checkbox v-model="forms.zach" label="Зачет (З)" />
          <q-checkbox v-model="forms.zacho" label="Зачет с оценкой (Зо)" />
          <q-checkbox v-model="forms.kp" label="Курсовой проект (КП)" />
          <q-checkbox v-model="forms.kr" label="Курсовая работа (КР)" />
        </div>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="Отмена" color="negative" @click="closeDialog" />
        <q-btn label="Сохранить" color="primary" @click="saveForms" :loading="store.saving" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
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

watch(() => props.modelValue, (val) => {
  showDialog.value = val
})

watch(showDialog, (val) => {
  emit('update:modelValue', val)
})

watch(() => props.editingData, (data) => {
  if (data.forms) {
    forms.value = {
      ekz: data.forms.includes('Э'),
      zach: data.forms.includes('З'),
      zacho: data.forms.includes('Зо'),
      kp: data.forms.includes('КП'),
      kr: data.forms.includes('КР')
    }
  }
}, { deep: true })

function closeDialog() {
  showDialog.value = false
  forms.value = {
    ekz: false,
    zach: false,
    zacho: false,
    kp: false,
    kr: false
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
    
    emit('saved')
    closeDialog()
  } catch (error) {
    console.error('Error saving forms:', error)
  }
}
</script>