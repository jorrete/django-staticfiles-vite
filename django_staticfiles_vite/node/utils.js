async function resolveId(id, paths) {
  for (let index = 0; index < paths.length; index++) {
    const path = paths[index];
    const match = await this.resolve(`${path}${id}`);
    if (match) {
      return match;
    }
  }
}

module.exports = {
  resolveId,
};
