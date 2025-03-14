<script setup lang="ts">

import {computed, onBeforeMount, ref} from "vue";
import {useQuasar} from "quasar";
import useMainStore from "stores/mainStore";
import {storeToRefs} from "pinia";
import {api} from "boot/axios";
import _ from "lodash";
import QSelectFilterable from "components/QSelectFilterable.vue";
import dayjs from "dayjs";
import usePlanViewStore from "stores/planViewStore";

const mainStore = useMainStore();
const {csrf, FORCE_SCRIPT_NAME} = storeToRefs(mainStore)

const planViewStore = usePlanViewStore();
const {files} = storeToRefs(planViewStore);


const uploading = ref(false);
const uploaderRef = ref();
const $q = useQuasar()
const uploadFileDialog = ref(false);
const allFilter = ref("");

const codes = computed(() => {
  let r = _(files.value).map(x => x.code).uniq().sortBy().value();
  return r;
})
const codeFilter = ref([]);

const abbrs = computed(() => {
  let r = _(files.value).map(x => x.abbr).uniq().sortBy().value();
  return r;
})
const abbrFilter = ref([]);

const years = computed(() => {
  let r = _(files.value).map(x => x.year).uniq().sortBy().value();
  return r;
})
const yearFilter = ref([]);


function removeFile(fileId: number) {
  $q.dialog({
    title: 'Удаление файла',
    message: 'Вы точно хотите отправить файл в архив?',
    ok: {
      label: 'В архив',
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
    let r = await api.delete(`api/plx/${fileId}`)
    $q.notify({
      type: 'secondary',
      message: `Файл удален :)  `,
    })
    await planViewStore.fetchPlxFiles()
  })

}


const filesFiltered = computed(() => {
  return files.value.filter(x => {
    return ((codeFilter.value || []).length == 0 || (codeFilter.value || []).includes(x.code))
      && ((abbrFilter.value || []).length == 0 || (abbrFilter.value || []).includes(x.abbr))
      && ((yearFilter.value || []).length == 0 || (yearFilter.value || []).includes(x.year))
    && (!allFilter.value || x.title.toLowerCase().includes(allFilter.value.toLowerCase()))
  })
})

function filefilter(files: File[]) {
  return files.filter(file => file.name.slice(file.name.lastIndexOf(".")) == ".plx")
}

function onRejected(rejectedEntries: any[]) {
  $q.notify({
    type: 'negative',
    message: `${rejectedEntries.length} файл не прошли проверку, загружайте только файла расширения .plx`,
  })
}

async function onUploadFinished() {
  uploading.value = false
  await planViewStore.fetchPlxFiles()
}

</script>

<template>

  <q-dialog v-model="uploadFileDialog">
    <q-card>
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">Загрузка PLX файлов</div>
        <q-space/>
        <q-btn icon="close" flat round dense v-close-popup/>
      </q-card-section>
      <q-card-section class="q-pt-none">
        <q-uploader
          ref="uploaderRef"
          class="uploader-container"
          flat
          color="white"
          text-color="black"
          auto-upload
          :url="`${FORCE_SCRIPT_NAME}/api/plx/insert-file/`"
          multiple
          accept=".plx"
          :filter="filefilter"
          :headers="[{name: 'X-CSRFToken', value: csrf}]"
          @rejected="onRejected"
          @start="uploading = true"
          @finish="onUploadFinished"
        >
        </q-uploader>
      </q-card-section>
    </q-card>
  </q-dialog>

  <div class="plx-container">
    <div class="q-pa-md" style="display: grid; grid-template-columns: 3fr 1fr 1fr 1fr auto; gap: 1rem">
      <q-input v-model="allFilter" label="Название" clearable></q-input>
      <q-select-filterable use-input filled clearable use-chips multiple :options="codes"
                v-model="codeFilter" label="Шифр"></q-select-filterable>
      <q-select-filterable use-input filled clearable use-chips multiple :options="abbrs"
                v-model="abbrFilter" label="Аббревиатура"></q-select-filterable>
      <q-select-filterable use-input filled clearable use-chips multiple :options="years"
                v-model="yearFilter" label="Год"></q-select-filterable>
      <q-btn color="purple-3" @click="uploadFileDialog = true">Загрузить PLX файлы</q-btn>
    </div>
    <div class="plx-table">
      <div class="plx-file-row plx-file-row__header">
        <div class="plx-file-cell">Название</div>
        <div class="plx-file-cell">Аббривеатура</div>
        <div class="plx-file-cell">Шифр</div>
        <div class="plx-file-cell">Год</div>
        <div class="plx-file-cell">Статус</div>
        <div class="plx-file-cell">Дата загрузки</div>
        <div class="plx-file-cell">Действие</div>
      </div>

      <div v-for="f in filesFiltered" class="plx-file-row">
        <div class="plx-file-cell" style="font-size: 1.25rem">
          <router-link :to="`/plx/${f.id}/disciplines`">{{ f.title }}</router-link>
        </div>
        <div class="plx-file-cell">{{ f.abbr }}</div>
        <div class="plx-file-cell">{{ f.code }}</div>
        <div class="plx-file-cell">{{ f.year }}</div>
        <div class="plx-file-cell">{{ f.status_verbose }}</div>
        <div class="plx-file-cell">{{ dayjs(f.created_at).format("YYYY-MM-DD HH:mm:ss") }}</div>
        <div class="plx-file-cell">
          <q-btn :disable="f.status == 'Проверен'" class="gt-xs" ripple dense round icon="mdi-delete" color="red"
                 @click="removeFile(f.id)"/>
        </div>
      </div>
    </div>
  </div>

</template>

<style lang="scss" scoped>

.plx-container {
  display: grid;
  grid-template-rows: auto 1fr;
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  right: 0;
}

.plx-table {
  display: grid;
  grid-template-columns: 1fr repeat(5, auto) auto;
  align-content: start;
  overflow: scroll;
  border-top: 1px solid silver;

  .plx-file-row {
    display: contents;

    &:hover {
      .plx-file-cell {
        background-color: $orange-1;
      }
    }

    &.plx-file-row__header {
      .plx-file-cell {
        background-color: white;
        z-index: 1;
        position: sticky;
        top: 0;
      }
    }
  }

  .plx-file-cell {
    padding: 1rem;
    border-bottom: 1px solid silver;
    border-right: 1px solid silver;
    display: flex;
    align-items: center;
    justify-content: center;

    transition: all .2s;
  }
}
</style>
