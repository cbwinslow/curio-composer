import React from 'react';

const UploadForm = () => {
  return (
    <form>
      <input type="file" accept="audio/*,video/*" />
      <input type="text" placeholder="Paste media URL" />
      <button type="submit">Upload</button>
    </form>
  );
};

export default UploadForm;
