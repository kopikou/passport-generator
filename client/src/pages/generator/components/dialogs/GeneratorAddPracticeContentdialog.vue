<script setup lang="ts">

import {useDialogPluginComponent} from "quasar";
import {computed, onBeforeMount, ref} from "vue";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import _, {add} from "lodash";

defineEmits([
  ...useDialogPluginComponent.emits
])

const {dialogRef, onDialogHide, onDialogOK, onDialogCancel} = useDialogPluginComponent()
const props = defineProps({
  id: {
    required: false,
    type: Number,
  },
})

const generatorViewStore = useGeneratorViewStore();

const {
  activeRpdId,
  additionalInfo,
} = storeToRefs(generatorViewStore)

const part = ref('')
const content = ref('')

const correct = computed(() => {
  if (!part.value || part.value.length < 4) return true
  if (!content.value || content.value.length < 4) return true

  return false
})

async function onOKClick() {
  const data = {
    content: content.value,
    part: part.value,
    id: props.id ? props.id : Math.floor(Math.random() * 100000),
  }
  onDialogOK(data)
}

onBeforeMount(() => {
  if (props.id) {
    const data = _(additionalInfo.value).filter(x => x.type == 'practiceContent').get('[0].value', []).find(x => x.id == props.id)
    content.value = data.content
    part.value = data.part
  }
})

</script>

<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide" persistent>
    <q-card class="q-dialog-plugin" style="width: 700px;">
      <q-card-section>
        <div class="text-h6">
          Добавить/обновить содержание этапа
        </div>
      </q-card-section>

      <q-separator/>

      <q-card-section>
        <div class="q-gutter-y-md">
          <q-input
            type="text"
            v-model="part"
            filled
            label="Этап"
            :rules="[val => val.length > 3 || 'Введите больше трех символов']"
          />
          <q-input
            type="textarea"
            v-model="content"
            filled
            label="Содержание работ"
            :rules="[val => val.length > 3 || 'Введите больше трех символов']"
          />
        </div>
      </q-card-section>

      <q-separator/>

      <q-card-actions align="right">
        <q-btn flat color="teal" label="Сохранить" @click="onOKClick" :disabled="correct"/>
        <q-btn flat color="red" label="Отмена" @click="onDialogCancel"/>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<style scoped>

</style>
