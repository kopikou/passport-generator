<script setup lang="ts">

import {computed, ref, watchEffect} from "vue";
import {useQuasar} from "quasar";
import GeneratorAddPracticeContentdialog
  from "pages/generator/components/dialogs/GeneratorAddPracticeContentdialog.vue";
import _ from "lodash";
import {api} from "boot/axios";
import {storeToRefs} from "pinia";
import useGeneratorViewStore from "stores/generatorViewStore";

const $q = useQuasar()

const generatorViewStore = useGeneratorViewStore();

const {
  activeRpdId,
  additionalInfo,
} = storeToRefs(generatorViewStore)

const content = ref()

const columns = ref([
  {name: 'num', label: '№ п/п', field: 'num', align: 'center', style: 'width: 50px', headerStyle: 'width: 50px'},
  {name: 'part', label: 'Этап', field: 'part', align: 'left'},
  {name: 'content', label: 'Содержание работ', field: 'content', align: 'left'},
  {
    name: 'settings',
    label: 'Управление',
    field: 'settings',
    align: 'center',
    style: 'width: 150px',
    headerStyle: 'width: 150px'
  },
])

const rows = ref([])

const filteredRows = computed(() => {
  return _.orderBy(rows.value, x => x.num)
})

const maxNumber = computed(() => {
  let data = _(rows.value).orderBy(x => x.num).last()
  if (data) {
    return data.num
  } else {
    return 1
  }
})

async function saveRow() {
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    type: 'practiceContent',
    value: rows.value,
  })

  await generatorViewStore.getData();
  // let key = _.findKey(additionalInfo.value, x => x.type == 'practiceContent')
  // if (key) {
  //   _.set(additionalInfo.value, key, r.data)
  // } else {
  //   additionalInfo.value.push(r.data)
  // }
}

function updateRow(id) {
  $q.dialog({
    component: GeneratorAddPracticeContentdialog,
    componentProps: {
      id: id,
    },
  }).onOk(async (data) => {
    let key = _.findKey(rows.value, x => x.id == id)
    const num = _.get(rows.value, key)?.num
    _.set(rows.value, key, {...data, num: num})
    saveRow()
  })
}

function deleteRow(id) {
  $q.dialog({
    title: 'Удаление этапа',
    message: 'Вы точно хотите удалить содержание этапа?',
    ok: {
      label: 'Удалить',
      flat: true,
      color: 'red',
    },
    cancel: {
      label: 'Отмена',
      flat: true,
      color: 'green',
    },
    persistent: true
  }).onOk(async () => {

    let key = _.findKey(rows.value, x => x.id == id)
    rows.value.splice(key, 1)

    saveRow()

  })
}

function addRow() {
  $q.dialog({
    component: GeneratorAddPracticeContentdialog,
  }).onOk(async (data) => {

    const num = _(rows.value).orderBy(x => x.num).last()

    if (!num) {
      rows.value.push({...data, num: 1})
    } else {
      rows.value.push({...data, num: num.num + 1})
    }

    saveRow()

  })
}

function moveCell(num, type) {
  if (type == 'up') {
    let newKey = _.findKey(rows.value, (x) => x.num == num - 1)
    let oldKey = _.findKey(rows.value, (x) => x.num == num)

    _.set(rows.value, `[${oldKey}].num`, num - 1)
    _.set(rows.value, `[${newKey}].num`, num)
  } else if (type == 'down') {
    let newKey = _.findKey(rows.value, (x) => x.num == num + 1)
    let oldKey = _.findKey(rows.value, (x) => x.num == num)

    _.set(rows.value, `[${oldKey}].num`, num + 1)
    _.set(rows.value, `[${newKey}].num`, num)
  }
  saveRow()
}

async function saveContent() {
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    type: 'practiceContentText',
    value: {
      content: content.value,
    }
  })

  $q.notify({
    message: "Данные <span class='text-bold'>о содержании практики</span> сохранены!",
    color: "secondary",
    position: "bottom",
    html: true,
  })
  await generatorViewStore.getData();

  // let key = _.findKey(additionalInfo.value, x => x.type == 'practiceContentText')
  // _.set(additionalInfo.value, `[${key}].value.content`, content.value)
}

watchEffect(() => {
  rows.value = _(additionalInfo.value).filter(x => x.type == 'practiceContent').get('[0].value', [])
  content.value = _(additionalInfo.value).filter(x => x.type == 'practiceContentText').get('[0].value.content', '')
})

</script>

<template>
  <div class="q-px-md">
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Содержание практики</span>
      <p></p>
      <q-separator class="q-mt-md q-mb-md"/>
      <div class="q-gutter-y-md q-mt-sm">
        <q-input
            label="Содержание практики"
            filled
            type="textarea"
            v-model="content"
            :debounce="500"
            @update:model-value="saveContent"
        />
        <div>

          <q-btn label="Добавить строчку" color="primary" class="q-mb-xs" @click="addRow"/>
          <q-table
              title="Содержание этапов"
              :columns="columns"
              :rows="filteredRows"
              :rows-per-page-options="[]"
              no-data-label="Не заполнено"
              bordered
          >
            <template #body-cell-settings="props">
              <q-td align="center">
                <q-btn
                    icon="mdi-delete" color="red" flat @click="deleteRow(props.row.id)" :disabled="disabled"
                />
                <q-btn
                    icon="mdi-update" color="green" flat @click="updateRow(props.row.id)" :disabled="disabled"
                />
                <q-btn v-if="props.row.num != 1"
                       icon="mdi-arrow-up-thin" color="black" flat :disabled="disabled"
                       @click="moveCell(props.row.num, 'up')"
                />
                <q-btn v-if="props.row.num != maxNumber"
                       icon="mdi-arrow-down-thin" color="black" flat :disabled="disabled"
                       @click="moveCell(props.row.num, 'down')"
                />
              </q-td>
            </template>

          </q-table>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
